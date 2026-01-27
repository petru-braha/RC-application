"""
Connection factory module.

RC-application runs using two threads.
One thread is used for the app client interface (GUI or CLI).
The other thread is used for the multiplexing loop.

This module is used by both threads.
Thread-safety was ensured by applying the queue pattern.

The client interface threads enques operations to be performed by the common selector.
The multiplexing loop thread dequeues and processes these operations.
"""
import flet as ft
from collections import deque
import selectors

import core
from frontend import Chat
from network import Connection

logger = core.get_logger(__name__)

# Directly using instances of Reactor provokes race-conditions.
# Should only be used by the multiplexing thread.
class Reactor:
    """
    Attributes:
        page (obj): The frontend page, if the application was launched in GUI mode.
                    It servers as a context for running async tasks i.e. printing output.
        conn_chat_dict (dict): A dictionary of connections and their corresponding chats.

        selector (obj): The selector used by the application.
        conns_to_reg (deque): A queue of connections to be added to the selector.
        conns_to_rem (deque): A queue of connections to be removed from the selector.
    
    In GUI mode, the chats are mandatory.
    They provide the possibility to print to the user's screen the network outputs.
    """
    
    def __init__(self, page: ft.Page | None = None) -> None:
        """
        Args:
            page (obj): The frontend page, if the application was launched in GUI mode.
        
        Raises:
            TypeError: if the application was launched in GUI mode and the page was not provided.
        """
        # Both must be of the same value.
        # i.e. CLI and no page / GUI and page.
        if core.IS_CLI != page is None:
            raise TypeError("The page must be provided (only) in GUI mode")
        
        self.page = page

        self.conn_chat_dict: dict[Connection, Chat | None] = {}
    
        self.selector = selectors.DefaultSelector()
        self.conns_to_reg: deque[Connection] = deque()
        self.conns_to_rem: deque[Connection] = deque()
        
    def add_conn(self, conn: Connection) -> None:
        """
        Registers a connection to the selector.
        https://docs.python.org/3/library/selectors.html#selectors.BaseSelector.register
        
        Closes the connection if it fails to be registered.
    
        Args:
            conn (obj): The connection to register.
        """
        try:
            self.selector.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE)
        except KeyError as e:
            logger.error(f"Failed to register connection {conn.addr}: {e}.")
            conn.close()
            logger.info(f"Closed connection {conn.addr}.")
        else:
            logger.info(f"Added connection {conn.addr} to selector.")

    def rem_conn(self, conn: Connection) -> None:
        """
        Removes a connection from the selector.
        "A file object shall be unregistered prior to being closed."
        https://docs.python.org/3/library/selectors.html#selectors.BaseSelector.unregister
    
        Args:
            conn (obj): The connection to remove.
        """
        try:
            self.selector.unregister(conn)
            self.conn_chat_dict.pop(conn)
        except (KeyError, ValueError) as e:
            logger.error(f"Failed to remove connection {conn.addr}: {e}.")
        else:
            logger.info(f"Removed connection {conn.addr} from selector.")
        finally:
            conn.close()
            logger.info(f"Closed connection {conn.addr}.")

    # See main.py --- `shutdown_app()`.
    # Doing `multiplexing_event.clear()` sends a signal to the multiplexing thread.
    # It will elegantly finish its last iteration before running the below function.
    # After all resources are cleared then the page is closed and destroyed.
    @core.uninterruptible
    def close_resources(self) -> None:
        """
        Removes any active connections and the selector.

        This function should be called right before exiting the application.
        """
        logger.info("Closing resources...")

        try:
            leftover_conns = set(self.conn_chat_dict.keys())
            if leftover_conns:
                logger.warning("Removing leftover active connections.")
            for conn in leftover_conns:
                logger.debug(f"Leftover connection: {conn}.")
                self.rem_conn(conn)
    
            conns_to_add_len = len(self.conns_to_reg)
            if conns_to_add_len > 0:
                logger.warning(f"Ignoring and closing {conns_to_add_len} conns enqueued to be added.")
            for conn in self.conns_to_reg:
                logger.debug(f"Ignoring connection: {conn}.")
                conn.close()
    
            conns_to_rem_len = len(self.conns_to_rem)
            if conns_to_rem_len > 0:
                logger.warning(f"Removing {conns_to_rem_len} conns enqueued to be removed.")
            for conn in self.conns_to_rem:
                logger.debug(f"Removing connection: {conn}.")
                self.rem_conn(conn)
    
            self.selector.close()
            logger.info("Resources closed.")

        except Exception as e:
            logger.critical(f"Failed to close resources: {e}.", exc_info=True)

class ReactorClient:
    """
    Client interface for the Reactor.
    
    This class provides a thread-safe way for the frontend to interact with the reactor (e.g. enqueue connections/commands).
    """

    def __init__(self, reactor: Reactor):
        self._reactor = reactor

    def enqueue_new_conn(self, conn_data: tuple) -> Connection:
        """
        Enqueues a new connection to be added to the selector.
        
        Raises:
            ConnectionCountError: If the maximum number of connections is reached.
        """
        conn = Connection(*conn_data)
        logger.info(f"Enqueuing connection {conn.addr} to be added.")
        self._reactor.conns_to_reg.append(conn)
        return conn
    
    # The below two methods are separated.
    # The Chat can not be created before the connection is,
    # and the bind is performed after the chat is created.
    def enqueue_cmd(self, conn: Connection, cmd: str) -> None:
        """
        Enqueues a command to be sent over the connection.
        """
        conn.sender.add_pending(cmd)

    def bind_chat(self, conn: Connection, chat: Chat) -> None:
        """
        Binds a Chat instance to a Connection.
        """
        self._reactor.conn_chat_dict[conn] = chat
    
    def enqueue_close_conn(self, conn: Connection) -> None:
        """
        Enqueues a connection to be closed and removed from the selector.
        """
        logger.info(f"Enqueuing connection {conn.addr} to be removed.")
        assert conn in self._reactor.conn_chat_dict.keys()
        self._reactor.conns_to_rem.append(conn)

"""
This module contains all the logic related to I/O multiplexing.

It is based on a central loop method supposed to run a on parallel thread.
This method selects the sockets ready for either reading/writing and dispatches them to their corresponding handlers.
"""
from selectors import EVENT_READ, EVENT_WRITE
from threading import Event
from time import sleep

import core
from frontend import Chat
from network import Connection
import transmission

from reactor import Reactor

logger = core.get_logger(__name__)

def loop_multiplexing(stay_alive: Event, reactor: Reactor, timeout: float | None = None) -> None:
    """
    The socket selection loop.
    
    One iteration first adds/removes enqued connections to application's selector,
    then selects ready sockets dispatching them to their corresponding handlers.

    Args:
        stay_alive (event): The event to signal the loop to continue/stop.
        reactor (obj): The reactor instance to use.
        timeout (float): The timeout for the selector.
    """
    _Multiplexer(stay_alive, reactor, timeout)

class _Multiplexer:
    """
    The main multiplexing loop class.

    It manages the event loop, handling connection queues and dispatching I/O events.
    """
    
    DEFAULT_TIMEOUT: float = 1
    """
    The default timeout for the event loop.
    """

    def __init__(self, stay_alive: Event, reactor: Reactor, timeout: float | None = None):
        self.stay_alive = stay_alive
        self.reactor = reactor
        self.timeout = timeout if timeout is not None else _Multiplexer.DEFAULT_TIMEOUT
        self.loop()

    @core.uninterruptible
    def loop(self) -> None:
        """
        Starts the event loop.
        """
        while self.stay_alive.is_set():
            try:
                self.handle_conn_queues()
                self.sel_and_dispatch()
            except Exception as e:
                logger.critical(f"Multiplexing loop error: {e}.", exc_info=True)
        # The event flag was cleared.
        # The application prepares to completely shutdown.
        self.reactor.close_resources()

    def handle_conn_queues(self) -> None:
        """
        Handles the interaction (add/removal) between the selector and enqueued connections.
        """
        while self.reactor.conns_to_reg:
            conn = self.reactor.conns_to_reg.popleft()
            self.reactor.add_conn(conn)
            
        while self.reactor.conns_to_rem:
            conn = self.reactor.conns_to_rem.popleft()
            self.reactor.rem_conn(conn)

    def sel_and_dispatch(self) -> None:
        """
        Polls for I/O events and dispatches them to the registered handlers.
        
        It also manages connection related issues.
        """
        # No need to run `select()` if there are no connections.
        if not self.reactor.selector.get_map():
            # Wait for a second, hoping that a client will enqueue a connection.
            # This was arbitrarily chosen.
            sleep(_Multiplexer.DEFAULT_TIMEOUT)
            return

        events = self.reactor.selector.select(self.timeout)
        for key, mask in events:
            
            conn = key.fileobj
            assert isinstance(conn, Connection)
            
            try:
                if mask & EVENT_READ:
                    self.sel_readable(conn)
                if mask & EVENT_WRITE:
                    self.sel_writable(conn)
        
            except ConnectionError as e:
                logger.warning(f"The connection {conn.addr} was closed by peer: {e}.")
                logger.info("Removing the connection.")
                self.reactor.rem_conn(conn)
                continue
            
            except Exception as e:
                logger.error(f"Failed to handle event for conn {conn.addr}: {e}.", exc_info=True)
                continue

    def sel_readable(self, conn: Connection) -> None:
        """
        Handles and processes readable sockets.

        It also manages partial operations results,
        and re-negotiates the protocol if necessary and possible (from RESP3 to RESP2)
        in case the server does not support the newer version.

        Args:
            conn (Connection): The connection to handle.
            chat (Chat | None): The chat associated with the connection.
        """
        try:
            assert conn.synchronizer.last_raw_input is not None
            output_str = transmission.handle_read(
                conn.addr,
                conn.receiver,
                conn.synchronizer.last_raw_input,
                conn.synchronizer.all_sent)
            
            self.cond_render(conn, output_str)
            conn.synchronizer.all_recv = True
    
        except core.PartialResponseError:
            logger.debug("The response is not completely received.")
        except core.PartialRequestError:
            logger.debug("The request is not completely sent.")
        # todo what if it is an auth error?
        except transmission.Resp3NotSupportedError:
            logger.warning("RESP3 not supported; retrying with RESP2.")
            conn.say_hello(conn.initial_user,
                                 conn.initial_pasw,
                                 core.RespVer.RESP2)

    def sel_writable(self, conn: Connection) -> None:
        """
        Handles and processes writable sockets and manages invalid input and partial response issues.
    
        Args:
            conn (Connection): The connection to handle.
            chat (Chat | None): The chat associated with the connection.
        """
        try:
            transmission.handle_write(
                conn.addr,
                conn.sender,
                conn.synchronizer)
        except core.PartialResponseError:
            logger.debug("The last result was not completely received.")
        except ValueError as e:
            # If the user makes an error, the error is both logged and printed on his screen as a response.
            logger.error(f"Error when encoding data to {conn.addr}: {e}.", exc_info=True)
            self.cond_render(conn, str(e))

    def cond_render(self, conn: Connection, res: str) -> None:
        """
        If the application was lauched in the GUI mode, it renders the response on the GUI.

        Args:
            conn (obj): The connection object.
            res (str): The response from either a network call or a client error.
        """
        if core.IS_CLI:
            return
        
        chat = self.reactor.conn_chat_dict[conn]
        assert chat is not None
        
        assert self.reactor.page is not None
        self.reactor.page.run_task(chat.add_res, res)

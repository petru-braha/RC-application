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

@core.uninterruptible
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

    def loop(self) -> None:
        """
        Starts the event loop.
        """
        while self.stay_alive.is_set():
            try:
                self.handle_connection_queues()
                self.sel_and_dispatch()
            except Exception as e:
                logger.critical(f"Multiplexing loop error: {e}.", exc_info=True)
        # The application prepares to completely shutdown.
        self.reactor.close_resources()

    def handle_connection_queues(self) -> None:
        """
        Handles the interaction (add/removal) between the selector and enqueued connections.
        """
        while self.reactor.connections_to_reg:
            connection = self.reactor.connections_to_reg.popleft()
            self.reactor.add_connection(connection)
            
        while self.reactor.connections_to_rem:
            connection = self.reactor.connections_to_rem.popleft()
            self.reactor.rem_connection(connection)

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
            
            connection = key.fileobj
            assert isinstance(connection, Connection)
            chat = self.reactor.conn_chat_dict[connection]
            
            try:
                if mask & EVENT_READ:
                    self.sel_readable(connection, chat)
                if mask & EVENT_WRITE:
                    self.sel_writable(connection, chat)
        
            except ConnectionError as e:
                logger.warning(f"The connection {connection.addr} was closed by peer: {e}.")
                logger.info("Removing the connection.")
                self.reactor.rem_connection(connection)
                continue
            
            except Exception as e:
                logger.error(f"Failed to handle event for connection {connection.addr}: {e}.", exc_info=True)
                continue

    def sel_readable(self, connection: Connection, chat: Chat | None) -> None:
        """
        Handles and processes readable sockets.

        It also manages partial operations results,
        and re-negotiates the protocol if necessary and possible (from RESP3 to RESP2)
        in case the server does not support the newer version.

        Args:
            connection (Connection): The connection to handle.
            chat (Chat | None): The chat associated with the connection.
        """
        try:
            output_str = transmission.handle_read(
                connection.addr,
                connection.receiver,
                connection.synchronizer.last_raw_input,
                connection.synchronizer.all_sent)
            self.reactor.page.run_task(chat.add_res, output_str)
            connection.synchronizer.all_recv = True
    
        except core.PartialResponseError:
            logger.debug("The response is not completely received.")
        except core.PartialRequestError:
            logger.debug("The request is not completely sent.")
        # todo what if it is an auth error?
        except transmission.Resp3NotSupportedError:
            logger.warning("RESP3 not supported; retrying with RESP2.")
            connection.say_hello(connection.initial_user,
                                 connection.initial_pasw,
                                 core.RespVer.RESP2)

    def sel_writable(self, connection: Connection, chat: Chat | None) -> None:
        """
        Handles and processes writable sockets and manages invalid input and partial response issues.
    
        Args:
            connection (Connection): The connection to handle.
            chat (Chat | None): The chat associated with the connection.
        """
        try:
            transmission.handle_write(
                connection.addr,
                connection.sender,
                connection.synchronizer)
        except core.PartialResponseError:
            logger.debug("The last result was not completely received.")
        except ValueError as e:
            # If the user makes an error, the error is both logged and printed on his screen as a response.
            logger.error(f"Error when encoding data to {connection.addr}: {e}.", exc_info=True)
            if chat is None:
                return
            self.reactor.page.run_task(chat.add_res, str(e))

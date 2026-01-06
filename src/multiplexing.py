"""
This module contains all the logic related to I/O multiplexing.

It is based on a central loop method supposed to run a on parallel thread.
This method selects the sockets ready for either reading/writing and dispatches them to their corresponding handlers.
"""
from selectors import EVENT_READ, EVENT_WRITE
from threading import Event
from time import sleep

from core import get_logger
from network import Connection
import transmission

import reactor

logger = get_logger(__name__)

_DEFAULT_TIMEOUT: float = 1
"""
The default timeout for the event loop.
"""

def run_multiplexing_loop(stay_alive: Event) -> None:
    """
    The socket selection loop.
    
    One iteration first adds/removes enqued connections to application's selector,
    then selects ready sockets dispatching them to their corresponding handlers.

    Args:
        stay_alive (obj): The event to signal the loop to continue/stop.
    """
    while stay_alive.is_set():
        try:
            _handle_connection_queues()
            _select_and_dispatch()
        except Exception as e:
            logger.critical(f"Multiplexing loop error: {e}.", exc_info=True)
    # The application prepares to completely shutdown.
    # Handle any remaining connections.

    logger.info("Closing selector...")
    _handle_connection_queues()
    reactor.close_selector()

def _handle_connection_queues() -> None:
    """
    Handles the interaction (add/removal) between the selector and enqueued connections.
    """
    while reactor._connections_to_add:
        connection, on_response = reactor._connections_to_add.popleft()
        reactor.add_connection(connection, on_response)
            
    while reactor._connections_to_rem:
        connection = reactor._connections_to_rem.popleft()
        reactor.rem_connection(connection)

def _select_and_dispatch(timeout: float = _DEFAULT_TIMEOUT) -> None:
    """
    Polls for I/O events and dispatches them to the registered handlers.
    
    Args:
        timeout: The maximum time to wait for events.
    """
    # No need to run `select()` if there are no connections.
    if not reactor._selector.get_map():
        # Wait for a second, hoping that a client will enqueue a connection.
        # This was arbitrarily chosen.
        sleep(_DEFAULT_TIMEOUT)
        return

    events = reactor._selector.select(timeout)
    for key, mask in events:
        try:
            connection = key.fileobj
            assert isinstance(connection, Connection)
            response_lambda = reactor._response_lambdas[connection]
            
            if mask & EVENT_READ:
                transmission.handle_read(connection, response_lambda)
            if mask & EVENT_WRITE:
                try:
                    transmission.handle_write(connection)
                except ValueError as e:
                    # If the user makes a syntax error.
                    # The error is both logged and printed on his screen as a response.
                    response_lambda(e)
                    logger.error(f"Error when encoding data to {str(connection.addr)}: {e}.", exc_info=True)
                    raise
        
        except ConnectionError as e:
            logger.warning(f"The connection {str(connection.addr)} was closed by peer: {e}.")
            logger.info("Removing the connection.")
            reactor.rem_connection(connection)
        
        except Exception as e:
            logger.error(f"Failed to handle event for connection {str(connection.addr)}: {e}.", exc_info=True)

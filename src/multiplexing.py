"""
This module contains all the logic related to I/O multiplexing.

It is based on a central loop method supposed to run a on parallel thread.
This method selects the sockets ready for either reading/writing and dispatches them to their corresponding handlers.
"""
from selectors import EVENT_READ, EVENT_WRITE
from threading import Event
from time import sleep
from typing import Callable

from core.config import get_logger
from core.exceptions import PartialResponseError, PartialRequestError
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
            _sel_and_dispatch()
        except Exception as e:
            logger.critical(f"Multiplexing loop error: {e}.", exc_info=True)
    # The application prepares to completely shutdown.
    # Handle any remaining connections.
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

def _sel_and_dispatch(timeout: float = _DEFAULT_TIMEOUT) -> None:
    """
    Polls for I/O events and dispatches them to the registered handlers.
    
    It also manages connection related issues.

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
                _sel_readable(connection, response_lambda)
            if mask & EVENT_WRITE:
                _sel_writable(connection, response_lambda)
        
        except ConnectionError as e:
            logger.warning(f"The connection {connection.addr} was closed by peer: {e}.")
            logger.info("Removing the connection.")
            reactor.rem_connection(connection)
            continue
        except Exception as e:
            logger.error(f"Failed to handle event for connection {connection.addr}: {str(e)}.", exc_info=True)
            continue

def _sel_readable(connection: Connection, response_lambda: Callable[[str], None]) -> None:
    """
    Handles and processes readable sockets.

    It also manages partial operations results,
    and re-negotiates the protocol if necessary and possible (from RESP3 to RESP2)
    in case the server does not support the newer version.
    
    Args:
        connection (obj): The connection to handle.
        response_lambda (lambda): The lambda function to forward the response to the client.
    """
    try:
        output_str = transmission.handle_read(
            connection.addr,
            connection.receiver,
            connection.synchronizer.last_raw_input,
            connection.synchronizer.all_sent)
        response_lambda(output_str)
        connection.synchronizer.all_recv = True
    
    except PartialResponseError:
        logger.debug("The response is not completely received.")
    except PartialRequestError:
        logger.debug("The request is not completely sent.")
    except transmission.Resp3NotSupportedError:
        logger.warning("RESP3 not supported; retrying with RESP2.")
        connection.say_hello(connection.initial_user,
                             connection.initial_pasw,
                             Connection.RESP2)

def _sel_writable(connection: Connection, response_lambda: Callable[[str], None]) -> None:
    """
    Handles and processes writable sockets and manages invalid input and partial response issues.
    
    Args:
        connection (obj): The connection to handle.
        response_lambda (lambda): The lambda function to forward potential input errors to the client.
    """
    try:
        transmission.handle_write(
            connection.addr,
            connection.sender,
            connection.synchronizer)
    except PartialResponseError:
        logger.debug("The last result was not completely received.")
    except ValueError as e:
        # If the user makes an error, the error is both logged and printed on his screen as a response.
        response_lambda(str(e))
        logger.error(f"Error when encoding data to {connection.addr}: {e}.", exc_info=True)

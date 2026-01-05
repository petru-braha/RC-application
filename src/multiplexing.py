"""
Dispatcher engine for I/O events.
Manages the event loop and delegates read/write operations to handlers.
"""

from selectors import EVENT_READ, EVENT_WRITE
from threading import Event
from time import sleep

from core import Config
from network import Connection
from transmission import handle_read, handle_write

import reactor

logger = Config.get_logger(__name__)

def run_multiplexing_loop(continue_loop_event: Event) -> None:
    """
    The main event loop for the operator.
    """
    while continue_loop_event.is_set():
        try:
            _handle_connection_queues()
            _tick()
        except Exception as e:
            logger.critical(f"Multiplexing loop error: {e}", exc_info=True)
    # Handle any remaining connections.
    _handle_connection_queues()

def _handle_connection_queues() -> None:
    """
    Handles the connection queues.
    """
    while reactor._connections_to_add:
        connection, on_response = reactor._connections_to_add.popleft()
        reactor.add_connection(connection, on_response)
            
    while reactor._connections_to_rem:
        connection = reactor._connections_to_rem.popleft()
        reactor.rem_connection(connection)

def _tick(timeout: float = DEFAULT_TIMEOUT) -> None:
    """
    Polls for I/O events and dispatches them to the registered handlers.
    
    Args:
        timeout: The maximum time to wait for events. None to wait indefinitely.
    """
    # On Windows, select() raises OSError if no file descriptors are registered.
    if not reactor._selector.get_map():
        sleep(timeout)
        return

    events = reactor._selector.select(timeout)
    for key, mask in events:
        connection = key.fileobj
        assert isinstance(connection, Connection)
        response_lambda = reactor._response_lambdas[connection]
        
        if mask & EVENT_READ:
            handle_read(connection.receiver, connection.synchronizer, response_lambda)
        if mask & EVENT_WRITE:
            handle_write(connection.sender, connection.synchronizer)

_DEFAULT_TIMEOUT: float = 1
"""
The default timeout for the event loop.
"""

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

from collections import deque
import selectors
from typing import Callable

from core import Config
from network import Connection

logger = Config.get_logger(__name__)

# Client modules should only call these functions.
def enque_new_connection(connection: Connection, on_response: Callable) -> None:
    """
    Enqueues a new connection to be added to the selector.
    """
    _connections_to_add.append((connection, on_response))

def enque_close_connection(connection: Connection) -> None:
    """
    Enqueues a connection to be removed from the selector.
    """
    _connections_to_rem.append(connection)

def close_application() -> None:
    """
    Closes Reactor selector and if there are any active connections,
    attempts to close them.
    """
    logger.info("Closing Reactor resources.")

    leftover_connections = set(_response_lambdas.keys())
    if leftover_connections:
        logger.warning("Some connections were not closed. Attempting to close them now.")
        logger.debug(f"Leftover connections: {leftover_connections}.")
    
    if _connections_to_add:
        logger.warning("Some connections were not added to the selector. Will not add them further.")
        logger.debug(f"Leftover connections to be added: {_connections_to_add}.")
    
    if _connections_to_rem:
        logger.warning("Some connections were not removed from the selector. Attempting to remove them now.")
        logger.debug(f"Leftover connections to be removed: {_connections_to_rem}.")
        for connection in _connections_to_rem:
            rem_connection(connection)

    try:
        _selector.close()
    except Exception as e:
        logger.error(f"Error closing selector: {e}.")

# Internal functions, calling them in the main thread might provoke race-conditions.
# These should be used only by the multiplexing thread.
def add_connection(connection: Connection, on_response: Callable) -> None:
    """
    Registers a connection to the Reactor.
    
    Args:
        connection (Connection): The connection to register.
        on_response (Callable): The callback function to be called when a response is received.
    """
    logger.debug(f"Registering connection {connection.addr} to Reactor.")
    _selector.register(connection.sock, selectors.EVENT_READ | selectors.EVENT_WRITE)
    _response_lambdas[connection] = on_response

def rem_connection(connection: Connection) -> None:
    """
    Removes a connection from the Reactor.
    
    Args:
        connection (Connection): The connection to remove.
    """
    logger.debug(f"Removing connection {connection.addr} from Reactor.")
    try:
        _selector.unregister(connection.sock)
        _response_lambdas.pop(connection)
    except (KeyError, ValueError) as e:
        logger.warning(f"Connection {connection.addr} not found: {e}.")
    connection.close()

_selector = selectors.DefaultSelector()
"""
A unique selector for the Reactor.
"""
_response_lambdas: dict[Connection, Callable[[str], None]] = {}
"""
Lambda functions for each connection to be called when a full response is received.
"""
_connections_to_add: deque[tuple[Connection, Callable]] = deque()
"""
A queue of connections to be added to the selector.
"""
_connections_to_rem: deque[Connection] = deque()
"""
A queue of connections to be removed from the selector.
"""

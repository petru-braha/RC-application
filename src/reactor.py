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

from core import get_logger
from network import Connection

logger = get_logger(__name__)

# Client modules should only call these functions.
def enque_new_connection(connection: Connection, on_response: Callable[[str], None]) -> None:
    """
    Enqueues a new connection to be added to the selector.
    """
    logger.info(f"Enqueuing connection {connection.addr} to be added.")
    _connections_to_add.append((connection, on_response))

def enque_close_connection(connection: Connection) -> None:
    """
    Enqueues a connection to be removed from the selector.
    """
    logger.info(f"Enqueuing connection {connection.addr} to be removed.")
    _connections_to_rem.append(connection)

# Calling these functions in the main thread provokes race-conditions.
# Should only be used by the multiplexing thread.
def close_selector() -> None:
    """
    Removes any active connections and closes the selector.

    This function should be called right before exiting the application.
    """
    logger.info("Closing resources.")

    try:
        leftover_connections = set(_response_lambdas.keys())
        if leftover_connections:
            logger.warning("Removing leftover active connections.")
            logger.debug(f"Leftover connections: {leftover_connections}.")
            for connection in leftover_connections:
                rem_connection(connection)
    
        connections_to_add_len = len(_connections_to_add)
        if connections_to_add_len:
            logger.warning(f"Ignoring and closing {connections_to_add_len} connections enqueued to be added.")
            logger.debug(f"Leftover connections to be added: {_connections_to_add}.")
            for connection, _ in _connections_to_add:
                connection.close()
    
        connections_to_rem_len = len(_connections_to_rem)
        if connections_to_rem_len:
            logger.warning(f"Removing {connections_to_rem_len} connections enqueued to be removed.")
            logger.debug(f"Leftover connections to be removed: {_connections_to_rem}.")
            for connection in _connections_to_rem:
                rem_connection(connection)
    
        _selector.close()
        logger.info("Resources closed.")

    except Exception as e:
        logger.critical(f"Failed to close resources: {e}.", exc_info=True)

def add_connection(connection: Connection, on_response: Callable) -> None:
    """
    Registers a connection to the selector.
    https://docs.python.org/3/library/selectors.html#selectors.BaseSelector.register
    
    Closes the connection if it fails to be registered.
    
    Args:
        connection (obj): The connection to register.
        on_response (lambda): The callback function to be called when a response is received.
    """
    try:
        _selector.register(connection, selectors.EVENT_READ | selectors.EVENT_WRITE)
        _response_lambdas[connection] = on_response
    except KeyError as e:
        logger.error(f"Failed to register connection {connection.addr}: {e}.")
        connection.close()
        logger.info(f"Closed connection {connection.addr}.")
    else:
        logger.info(f"Added connection {connection.addr} to selector.")

def rem_connection(connection: Connection) -> None:
    """
    Removes a connection from the selector.
    "A file object shall be unregistered prior to being closed."
    https://docs.python.org/3/library/selectors.html#selectors.BaseSelector.unregister
    
    Args:
        connection (obj): The connection to remove.
    """
    try:
        _selector.unregister(connection)
        _response_lambdas.pop(connection)
    except (KeyError, ValueError) as e:
        logger.error(f"Failed to remove connection {connection.addr}: {e}.")
    else:
        logger.info(f"Removed connection {connection.addr} from selector.")
    finally:
        connection.close()
        logger.info(f"Closed connection {connection.addr}.")

_selector = selectors.DefaultSelector()
"""
The unique selector used by the application.
"""
_response_lambdas: dict[Connection, Callable[[str], None]] = {}
"""
Lambda functions for each connection to be called when a full response is received.
"""
_connections_to_add: deque[tuple[Connection, Callable[[str], None]]] = deque()
"""
A queue of connections to be added to the selector.
"""
_connections_to_rem: deque[Connection] = deque()
"""
A queue of connections to be removed from the selector.
"""

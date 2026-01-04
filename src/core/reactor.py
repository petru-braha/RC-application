import selectors
from typing import Callable

from network import Connection

from .config import Config

logger = Config.get_logger(__name__)

class Reactor:
    """
    Connection factory class.

    Base class for I/O multiplexing.
    """
    
    _response_lambdas: dict[Connection, Callable[[str], None]]
    """
    """
    _selector: selectors.BaseSelector
    """
    """

    @staticmethod
    def start() -> None:
        logger.info("Initializing Reactor resources.")
        Reactor._selector = selectors.DefaultSelector()
        Reactor._response_lambdas = {}

    @staticmethod
    def close() -> None:
        logger.info("Closing Reactor resources.")
        try:
            Reactor._selector.close()
        except Exception as e:
            logger.error(f"Error closing selector: {e}.")
    
    @staticmethod
    def register_connection(connection: Connection, on_response: Callable) -> None:
        logger.debug(f"Registering connection {connection.addr} to Reactor.")
        Reactor._selector.register(connection, selectors.EVENT_READ | selectors.EVENT_WRITE)
        Reactor._response_lambdas[connection] = on_response
    
    @staticmethod
    def remove_connection(connection: Connection) -> None:
        logger.debug(f"Removing connection {connection.addr} from Reactor.")
        try:
            Reactor._selector.unregister(connection)
            Reactor._response_lambdas.pop(connection)
        except (KeyError, ValueError) as e:
             logger.warning(f"Connection {connection.addr} not found: {e}.")
        connection.close()

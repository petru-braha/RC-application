import selectors
from typing import Callable

from network import Connection

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
        Reactor._selector = selectors.DefaultSelector()
        Reactor._response_lambdas = {}

    @staticmethod
    def close() -> None:
        Reactor._selector.close()
    
    @staticmethod
    def register_connection(connection: Connection, on_response: Callable) -> None:
        Reactor._selector.register(connection)
        Reactor._response_lambdas[connection] = on_response
    
    @staticmethod
    def remove_connection(connection: Connection) -> None:
        Reactor._selector.unregister(connection)
        Reactor._response_lambdas.pop(connection)
        connection.close()

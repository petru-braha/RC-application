import selectors

from network import Connection

from constants import EMPTY_STR

class Reactor:
    """
    Connection factory class.

    Base class for I/O multiplexing.
    """
    
    _selector: selectors.BaseSelector
    """
    """

    @staticmethod
    def start() -> None:
        Reactor._selector = selectors.DefaultSelector()

    @staticmethod
    def close():
        Reactor._selector.close()
    
    @staticmethod
    def add_connection(host: str = EMPTY_STR,
                       port: str = EMPTY_STR,
                       user: str = EMPTY_STR,
                       pasw: str = EMPTY_STR,
                       db_idx: str = EMPTY_STR) -> Connection:
        connection = Connection(host, port, user, pasw, db_idx)
        Reactor._selector.register(connection)
        return connection

    @staticmethod
    def rem_connection(connection: Connection):
        connection.close()
        Reactor._selector.unregister(connection)

import selectors

from network import Connection

from constants import EMPTY_STR

class Reactor:
    """
    Connection factory class.

    Base class for I/O multiplexing.
    """
    
    def __init__(self):
        self.selector = selectors.DefaultSelector()

    def close(self):
        self.selector.close()
    
    def add_connection(self,
                       host: str = EMPTY_STR,
                       port: str = EMPTY_STR,
                       user: str = EMPTY_STR,
                       pasw: str = EMPTY_STR,
                       db_idx: str = EMPTY_STR) -> Connection:
        connection = Connection(host, port, user, pasw, db_idx)
        self.selector.register(connection)
        return connection

    def rem_connection(self, connection: Connection):
        connection.close()
        self.selector.unregister(connection)

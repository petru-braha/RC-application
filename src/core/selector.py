import selectors

from network import Connection

class Selector:
    _EVENT_MASK = selectors.EVENT_READ | selectors.EVENT_WRITE
    """
    Default event mask to be carried within selection process.
    """
    _SELECTOR: selectors.BaseSelector
    """
    Selector object used for I/O multiplexing.
    """
    
    @staticmethod
    def open() -> None:
        Selector._SELECTOR = selectors.DefaultSelector()

    @staticmethod
    def close() -> None:
        """
        Closes the selector.
        """
        Selector._SELECTOR.close()

    @staticmethod
    def register(conn: Connection) -> None:
        """
        Registers a created socket to be monitored for both readability and writability.
        """
        Selector._SELECTOR.register(conn, Selector._EVENT_MASK)

    @staticmethod
    def unregister(conn: Connection) -> None:
        """
        Unregisters a socket from monitoring.
        """
        Selector._SELECTOR.unregister(conn)

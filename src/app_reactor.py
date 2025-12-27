import selectors

from .network import Sock
from .transport import Receiver, Sender

from .app_state import _AppState

class AppReactor(_AppState):
    """
    Event loop manager using the most efficient I/O multiplexing mechanism
    available on the system (epoll, kqueue, select, etc.).
    """

    _EVENT_MASK = selectors.EVENT_READ | selectors.EVENT_WRITE
    """
    Default event mask to be carried within selection process.
    """
    _SELECTOR = selectors.DefaultSelector()
    """
    Selector object used for I/O multiplexing.
    """

    @staticmethod
    def close() -> None:
        """
        Closes the selector.
        """
        AppReactor._SELECTOR.close()

    @staticmethod
    def register(sock: Sock) -> None:
        """
        Registers a created socket to be monitored for both readability and writability.
        """
        AppReactor._sock_hist_dict[sock]
        AppReactor._SELECTOR.register(sock, AppReactor._EVENT_MASK)
        Receiver.register(sock)
        Sender.register(sock)

    @staticmethod
    def unregister(sock: Sock) -> None:
        """
        Unregisters a socket from monitoring.
        """
        try:
            del AppReactor._sock_hist_dict[sock]
            AppReactor._SELECTOR.unregister(sock)
            Receiver.unregister(sock)
            Sender.unregister(sock)
            sock.close()
            # todo check leftovers

        except (KeyError, ValueError):
            # Socket already unregistered or closed.
            pass

    @staticmethod
    def caputure_cmd(sock: Sock, msg: str):
        Sender.append_cmd(sock, msg)

    @staticmethod
    def tick(timeout: float | None = None) -> None:
        """
        Polls for I/O events and dispatches them to the registered handlers.
        
        Args:
            timeout: The maximum time to wait for events. None to wait indefinitely.
        """
        events = AppReactor._SELECTOR.select(timeout=timeout)
        for key, mask in events:
            
            sock = key.fileobj
            assert isinstance(sock, Sock)
            
            if mask & selectors.EVENT_READ:
                AppReactor._handle_read(sock)
            if mask & selectors.EVENT_WRITE:
                AppReactor._handle_write(sock)

    @staticmethod
    def _handle_read(sock: Sock) -> None:
        pass
        # Receiver.consume() # tries to decode
        # Receiver.recv() # if decoder fails
        # try to decode
        # update history
        # Page.update()

    @staticmethod
    def _handle_write(sock: Sock) -> None:
        # takes the first message to queue
        msg = ''
        bytes = msg.encode("ascii")
        sock.sendall(bytes)

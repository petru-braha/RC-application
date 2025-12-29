import selectors
import threading

from network import Connection, Receiver, Sender

from .specs import Specs
from .selector_holder import SelectorHolder

class Reactor(Specs):
    """
    Event loop manager using the most efficient I/O multiplexing mechanism
    available on the system (epoll, kqueue, select, etc.).
    """

    @staticmethod
    def start() -> None:
        def run():
            while True:
                try:
                    Reactor._tick(timeout=1)
                except Exception as e:
                    print(f"Reactor loop error: {e}")
        
        threading.Thread(target=run, daemon=True).start()

    @staticmethod
    def _tick(timeout: float | None = None) -> None:
        """
        Polls for I/O events and dispatches them to the registered handlers.
        
        Args:
            timeout: The maximum time to wait for events. None to wait indefinitely.
        """
        events = SelectorHolder.SELECTOR.select(timeout=timeout)
        for key, mask in events:
            
            conn = key.fileobj
            assert isinstance(conn, Connection)
            
            if mask & selectors.EVENT_READ:
                Reactor._handle_read(conn)
            if mask & selectors.EVENT_WRITE:
                Reactor._handle_write(conn)

    @staticmethod
    def _handle_read(conn: Receiver) -> None:
        """
        Reads from the socket, decodes data, and updates history.
        """
        is_empty = conn.empty_buf()
        
        # 1. Read from socket to buffer
        bytes_read = conn.recv()
        
        # 2. Decode and Archive if we have data
        if not conn.empty_buf():
            # Simplistic decoding for now as per previous context
            try:
                # Example:
                # data = conn.consume_crlf()
                # conn.archive(...)
                pass
            except Exception:
                pass

    @staticmethod
    def _handle_write(conn: Sender) -> None:
        """
        Sends pending commands to the socket.
        """
        conn.send_first()

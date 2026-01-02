import selectors
from threading import Thread

from network import Connection, Receiver, Sender

from .reactor import Reactor

class Operator(Reactor, Thread):
        
    def __init__(self):
        Reactor.__init__(self)
        Thread.__init__(self, target=self._run, daemon=True)
        self.start()

    def _run(self):
        while True:
            try:
                self._tick(timeout=1)
            except Exception as e:
                print(f"Reactor loop error: {e}")

    def _tick(self, timeout: float | None = None) -> None:
        """
        Polls for I/O events and dispatches them to the registered handlers.
        
        Args:
            timeout: The maximum time to wait for events. None to wait indefinitely.
        """
        # todo
        return
        events = self.selector.select(timeout)
        for key, mask in events:
            
            conn = key.fileobj
            assert isinstance(conn, Connection)
            if mask & selectors.EVENT_READ:
                Reactor._handle_read(conn)
            if mask & selectors.EVENT_WRITE:
                Reactor._handle_write(conn)

    def _handle_read(self, conn: Receiver) -> None:
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
    
    def _handle_write(self, conn: Sender) -> None:
        """
        Sends pending commands to the socket.
        """
        conn.send_first()

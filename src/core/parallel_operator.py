import selectors
from threading import Thread

from network import Connection, Receiver, Sender

from .reactor import Reactor

class Operator(Reactor, Thread):

    @staticmethod
    def start() -> None:
        Reactor.start()
        Thread(target=Operator._run, daemon=True).start()

    @staticmethod
    def _run():
        while True:
            try:
                Operator._tick(timeout=1)
            except Exception as e:
                print(f"Reactor loop error: {e}")

    @staticmethod
    def _tick(timeout: float | None = None) -> None:
        """
        Polls for I/O events and dispatches them to the registered handlers.
        
        Args:
            timeout: The maximum time to wait for events. None to wait indefinitely.
        """
        # todo
        return
        events = Operator.selector.select(timeout)
        for key, mask in events:
            
            conn = key.fileobj
            assert isinstance(conn, Connection)
            if mask & selectors.EVENT_READ:
                Operator._handle_read(conn)
            if mask & selectors.EVENT_WRITE:
                Operator._handle_write(conn)

    @staticmethod
    def _handle_read(conn: Receiver) -> None:
        """
        Reads from the socket, decodes data, and updates history.
        """
        is_empty = conn.empty_buf()
        bytes_read = conn.recv()
        
        if not conn.empty_buf():
            # Simplistic decoding for now as per previous context
            try:
                # Example:
                # data = conn.consume_crlf()
                # conn.archive(...)
                pass
            except Exception:
                pass
        
        # Display to the output
        Operator._response_lambdas[conn](value_read)
    
    @staticmethod
    def _handle_write(conn: Sender) -> None:
        """
        Sends pending commands to the socket.
        """
        conn.send_first()

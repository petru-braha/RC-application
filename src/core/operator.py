import selectors
from threading import Thread

from network import Connection
from protocol import decoder
from util import process_input

from exceptions import PartialResponseError

from .reactor import Reactor

class Operator(Reactor):
    """
    Dispatcher engine for I/O events.
    Manages the event loop and delegates read/write operations to handlers.
    """

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
        events = Operator.selector.select(timeout)
        for key, mask in events:
            
            connection = key.fileobj
            assert isinstance(connection, Connection)
            
            if mask & selectors.EVENT_READ:
                Operator._handle_read(connection)
            if mask & selectors.EVENT_WRITE:
                Operator._handle_write(connection)

    @staticmethod
    def _handle_read(connection: Connection) -> None:
        """
        Reads from the socket, decodes data, and updates history.

        Args:
            connection (Connection): The connection object to read from.
        """
        try:
            initial_buf_idx = connection._buf_idx
            output = decoder(connection)
            Operator._response_lambdas[connection](output)
        
        except PartialResponseError:
            connection._buf_idx = initial_buf_idx
            bytes_read = connection.recv()
        except (Exception, AssertionError):
            pass
    
    @staticmethod
    def _handle_write(connection: Connection) -> None:
        """
        Sends pending commands to the socket.
        
        Handles encoding of strings and manages partial sends by updating
        the connection's pending input queue.

        Args:
           connection (Connection): The connection object to write to.
        """
        if not connection.has_pending():
            return

        pending = connection.get_first_pending()
        
        # When partial send occurs,
        # the first pending input becomes the remaining bytes from the previous call.
        if isinstance(pending, str):
            encoded = process_input(pending)
        else:
            encoded = pending

        try:
            sent_count = connection.send(encoded)
        except BlockingIOError:
            # todo log
            return
        except OSError:
            # todo delete the socket yourself...
            return
        
        if sent_count >= len(encoded):
            connection.rem_first_pending()
            return

        # The command was not sent in one go.
        # Update the pending item with the remaining bytes.
        remaining = encoded[sent_count:]
        connection.shrink_first_pending(remaining)

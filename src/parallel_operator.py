from selectors import EVENT_READ, EVENT_WRITE
from time import sleep
from threading import Thread

from core import Config, PartialResponseError
from network import Connection

from reactor import Reactor
from util import process_input, process_output

logger = Config.get_logger(__name__)

class ParallelOperator(Reactor):
    """
    Dispatcher engine for I/O events.
    Manages the event loop and delegates read/write operations to handlers.
    """

    DEFAULT_TIMEOUT: float = 1
    """
    The default timeout for the event loop.
    """

    @staticmethod
    def start() -> None:
        Reactor.start()
        logger.info("Starting Operator event loop thread.")
        Thread(target=Operator._run, daemon=True).start()

    @staticmethod
    def _run():
        while True:
            try:
                Operator._tick()
            except Exception as e:
                logger.critical(f"Operator loop error: {e}", exc_info=True)

    @staticmethod
    def _tick(timeout: float = DEFAULT_TIMEOUT) -> None:
        """
        Polls for I/O events and dispatches them to the registered handlers.
        
        Args:
            timeout: The maximum time to wait for events. None to wait indefinitely.
        """
        # On Windows, select() raises OSError if no file descriptors are registered.
        if not Operator._selector.get_map():
            sleep(timeout)
            return

        events = Operator._selector.select(timeout)
        for key, mask in events:
            
            connection = key.fileobj
            assert isinstance(connection, Connection)
            
            if mask & EVENT_READ:
                Operator._handle_read(connection)
            if mask & EVENT_WRITE:
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
            
            logger.debug(f"Reflected: {output}.")
            Operator._response_lambdas[connection](output)
        
        # When a partial response is encountered, 
        # the buffer index is rolled back to the initial position, 
        # and the next chunk of data is read and concatenated to the initial buffer. 
        except PartialResponseError as e:
            logger.debug(f"Partial output received: {e}.")
            logger.debug(f"Rolling back {connection._buf_idx - initial_buf_idx} bytes.")
            connection._buf_idx = initial_buf_idx
            try:
                connection.recv()
            except BlockingIOError:
                logger.debug("Receiving would block.")
                return
            except Exception as e:
                logger.error(f"Error receiving data from {connection.addr}: {e}.")
                return

        except Exception as e:
            logger.error(f"Error when decoding data from {connection.addr}: {e}.", exc_info=True)
    
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
            try:
                encoded = process_input(pending)
            except Exception as e:
                logger.error(f"Error when encoding data to {connection.addr}: {e}.", exc_info=True)
                return
        else:
            logger.debug(f"Sending leftovers from a previous command: {pending}.")
            encoded = pending

        try:
            sent_count = connection.send(encoded)
            logger.debug(f"Sent {sent_count} bytes to {connection.addr}")
        except BlockingIOError:
            logger.debug("Sending would block.")
            return
        except OSError as e:
            logger.error(f"Write error on {connection.addr}: {e}. Remove the connection if closed.")
            return
        
        if sent_count >= len(encoded):
            connection.rem_first_pending()
            return

        # The command was not sent in one go.
        # Update the pending item with the remaining bytes.
        logger.debug(f"Partial send for {connection.addr}: {sent_count}/{len(encoded)} bytes sent.")
        remaining = encoded[sent_count:]
        connection.shrink_first_pending(remaining)

from typing import Callable

from core.config import get_logger
from core.exceptions import PartialResponseError
from network import Connection

from .processor import process_output, process_transmission

logger = get_logger(__name__)

def handle_read(connection: Connection, response_lambda: Callable[[str], None]) -> None:
    """
    Reads from the socket, decodes data, and updates history.

    Args:
        connection (obj): The connection object.
        response_lambda (lambda): The callback function for the response.

    Raises:
        ConnectionError: If the socket is closed by the peer.
    """
    if connection.synchronizer.all_sent != True:
        # This should never read bytes theoretically.
        # Reductio ad absurdum there are non-null amount of bytes; then read those.
        _handle_recv(connection)
        return
    
    def job():
        output = process_output(connection.receiver)
        process_transmission(connection, connection.synchronizer.last_raw_input, output)
        
        response_lambda(str(output))
        connection.synchronizer.all_recv = True

    try:
        initial_buf_idx = connection.receiver._idx
        job()
        
    # When a partial response is encountered, 
    # the buffer index is restored to the initial position, 
    # and the next chunk of data is read and concatenated to the initial buffer. 
    except PartialResponseError as e:
        connection.receiver.restore_buf(initial_buf_idx)
        _handle_recv(connection)
        try:
            job()
        except PartialResponseError:
            pass

def _handle_recv(connection: Connection) -> None:
    """
    Handles receiving data from the socket.

    Raises:
        ConnectionError: If the socket is closed by the peer.
    """
    try:
        connection.receiver.recv()
    except BlockingIOError:
        logger.warning("Receiving would block.")
    except ConnectionError as e:
        logger.error(f"Error receiving data from {str(connection.addr)}: {e}.")
        raise

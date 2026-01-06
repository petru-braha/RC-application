from core.config import get_logger
from core.exceptions import PartialResponseError, PartialRequestError
from core.structs import Address
from network import Receiver

from .processor import process_output, process_transmission
from .exceptions import Resp3NotSupportedError

logger = get_logger(__name__)

def handle_read(addr: Address, receiver: Receiver, last_raw_input: str, all_sent: bool) -> str:
    """
    Reads from the socket, decodes data, and updates history.

    Args:
        addr (obj): The address of the client.
        receiver (obj): The receiver object.
        last_raw_input (str): The last raw input.
        all_sent (bool): Whether the request is completely sent.

    Returns:
        str: The response to send to the client.
    
    Raises:
        PartialRequestError: If the request is not completely sent.
        PartialResponseError: If the response is not completely received.
        Resp3NotSupportedError: If the third protocol version is not supported by the remote instance.
        ConnectionError: If the socket is closed by the peer.
    """
    # If the input was not completely sent,
    # `recv()` should NOT read bytes theoretically.
    # Reductio ad absurdum there are bytes to be read; then do it.
    _handle_recv(receiver, addr)
    if all_sent != True:
        raise PartialRequestError("The request is not completely sent")
    
    try:
        initial_buf_idx = receiver._idx
        output = process_output(receiver)
        process_transmission(last_raw_input, output)
        output_str = str(output)
        return output_str
    
    # When a partial response is encountered, 
    # the buffer index is restored to the initial position, 
    # and the next chunk of data is read and concatenated to the initial buffer. 
    except PartialResponseError:
        receiver.restore_buf(initial_buf_idx)
        raise

def _handle_recv(receiver: Receiver, addr: Address) -> None:
    """
    Handles receiving data from the socket.

    Raises:
        ConnectionError: If the socket is closed by the peer.
    """
    try:
        receiver.recv()
    except BlockingIOError:
        logger.warning("Receiving would block.")
    except ConnectionError as e:
        logger.error(f"Error receiving data from {connection.addr}: {e}.")
        raise

import core
from network import Receiver

from .processor import process_output, is_init_command, validate_init_cmd_output

logger = core.get_logger(__name__)

def handle_read(addr: core.Addr, receiver: Receiver, last_raw_cmd: str, all_sent: bool | None) -> str:
    """
    Reads from the socket, decodes data, and updates history.

    Args:
        addr (obj): The address of the client.
        receiver (obj): The receiver object.
        last_raw_cmd (str): The last raw user input.
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
        raise core.PartialRequestError("The request is not completely sent")
    
    initial_buf_idx = receiver._idx
    try:
        output = process_output(receiver)
        if is_init_command(last_raw_cmd):
            validate_init_cmd_output(last_raw_cmd, output)
        return str(output)
    
    # When a partial response is encountered, 
    # the buffer index is restored to the initial position, 
    # and the next chunk of data is read and concatenated to the initial buffer. 
    except core.PartialResponseError:
        receiver.restore_buf(initial_buf_idx)
        raise

def _handle_recv(receiver: Receiver, addr: core.Addr) -> None:
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
        logger.error(f"Error receiving data from {addr}: {e}.")
        raise

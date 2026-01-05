from core.config import get_logger
from network import Connection

from .processor import process_input

logger = get_logger(__name__)

def handle_write(connection: Connection) -> None:
    """
    Sends pending commands to the socket.
    
    Handles encoding of strings and manages partial sends by updating
    the sender's pending input queue.

    Args:
        connection (obj): The connection object.

    Raises:
        ValueError: If the input is has parser errors.
        ConnectionError: If the socket is closed by the peer.
    """
    pending = connection.sender.get_first_pending()
    
    # Encoding the command.
    if pending == None:
        return
    # Note that an input might be transmitted by n number of `send()` calls.
    # When partial send occurs,
    # the first pending input from the queue becomes the remaining bytes from the `send()` call.
    if isinstance(pending, bytes):
        logger.debug(f"Sending leftovers from a previous command: {pending}.")
        encoded = pending
    else:
        assert isinstance(pending, str)
        # If the previous command was not fully received by the peer,
        # do NOT send this one.
        if connection.synchronizer.all_recv != True:
            logger.debug(
                f"Not sending {pending} to {str(connection.addr)} yet.\n"
                "Waiting for the previous command to be fully received.")
            return
        connection.synchronizer.sync_input(pending)
        # This might raise ValueError.
        encoded = process_input(pending)

    # Sending the command.
    _handle_send(connection, encoded)

def _handle_send(connection: Connection, encoded: bytes) -> None:
    """
    Handles sending data to the socket.

    Raises:
        ConnectionError: If the socket is closed by the peer.
    """
    try:
        sent_count = connection.sender.send(encoded)
    except BlockingIOError:
        logger.warning("Sending would block.")
        return
    except ConnectionError as e:
        logger.error(f"Error sending data to {str(connection.addr)}: {e}.")
        raise
    
    if sent_count >= len(encoded):
        connection.synchronizer.all_sent = True
        connection.sender.rem_first_pending()
        return

    # The command was not sent in one go.
    # Update the pending item with the remaining bytes.
    logger.debug(f"Partial send for {connection.addr}: {sent_count}/{len(encoded)} bytes sent.")
    remaining = encoded[sent_count:]
    connection.sender.shrink_first_pending(remaining)

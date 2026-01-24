import core
from network import Sender, Synchronizer

from .processor import process_input

logger = core.get_logger(__name__)

def handle_write(addr: core.Addr, sender: Sender, synchronizer: Synchronizer) -> None:
    """
    Sends pending commands to the socket.
    
    Handles encoding of strings and manages partial sends by updating
    the sender's pending input queue.

    Args:
        addr (obj): The address of the connection.
        sender (obj): The sender object.
        synchronizer (obj): The synchronizer object.

    Raises:
        PartialResponseError: If the last output was not fully received.
        ValueError: If the input is has parser errors.
        ConnectionError: If the socket is closed by the peer.
    """
    pending = sender.get_first_pending()
    
    # Encoding the command.
    if pending is None:
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
        if synchronizer.all_recv == False:
            raise core.PartialResponseError("The previous command's result was not fully received")
        
        logger.debug(f"Syncing input for {addr}: {pending}.")
        synchronizer.sync_input(pending)
        try:
            encoded = process_input(pending)
        except ValueError as e:
            logger.error(f"Input processing failed: {e}.")
            logger.info("Unsyncing and removing the input from pending commands to send.")
            synchronizer.unsync()
            sender.rem_first_pending()
            raise

    # Sending the command.
    _handle_send(addr, sender, synchronizer, encoded)

def _handle_send(addr: core.Addr, sender: Sender, synchronizer: Synchronizer, encoded: bytes) -> None:
    """
    Handles sending data to the socket.

    Raises:
        ConnectionError: If the socket is closed by the peer.
    """
    try:
        sent_count = sender.send(encoded)
    except BlockingIOError:
        logger.warning("Sending would block.")
        return
    except ConnectionError as e:
        logger.error(f"Error sending data to {addr}: {e}.")
        raise
    
    if sent_count >= len(encoded):
        synchronizer.all_sent = True
        sender.rem_first_pending()
        return

    # The command was not sent in one go.
    # Update the pending item with the remaining bytes.
    logger.debug(f"Partial send for {addr}: {sent_count}/{len(encoded)} bytes sent.")
    remaining = encoded[sent_count:]
    sender.shrink_first_pending(remaining)

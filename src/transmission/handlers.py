from typing import Callable

from core import Config, PartialResponseError
from network import Receiver, Sender, Synchronizer

from .processor import process_input, process_output, process_transmission

logger = Config.get_logger(__name__)

def handle_read(receiver: Receiver, synchronizer: Synchronizer, response_lambda: Callable[[str], None]) -> None:
    """
    Reads from the socket, decodes data, and updates history.

    Args:
        receiver (obj): The receiver object to read from.
        synchronizer (obj): The synchronizer object to use.
    """
    if synchronizer.all_sent != True:
        return
    
    try:
        initial_buf_idx = receiver._buf_idx
        output = process_output(receiver)
        process_transmission(synchronizer.last_raw_input, output)
            
        response_lambda(output)
        synchronizer.all_recv = True
        
        # When a partial response is encountered, 
        # the buffer index is restored to the initial position, 
        # and the next chunk of data is read and concatenated to the initial buffer. 
    except PartialResponseError as e:
        receiver.restore_buf(initial_buf_idx)
        try:
            receiver.recv()
        except BlockingIOError:
            logger.warning("Receiving would block.")
            return
        except Exception as e:
            logger.error(f"Error receiving data from {receiver.addr}: {e}.")
            return

    except Exception as e:
        logger.error(f"Error when decoding data from {receiver.addr}: {e}.", exc_info=True)

def handle_write(sender: Sender, synchronizer: Synchronizer) -> None:
    """
    Sends pending commands to the socket.
    
    Handles encoding of strings and manages partial sends by updating
    the sender's pending input queue.

    Args:
        sender (obj): The sender object to write to.
        synchronizer (obj): The synchronizer object to use.
    """
    if not sender.has_pending():
        return

    pending = sender.get_first_pending()
    
    # When partial send occurs,
    # the first pending input becomes the remaining bytes from the previous call.
    if isinstance(pending, str):

        #! Pretty important call.
        if synchronizer.all_recv != True:
            logger.debug(f"Partial send for {sender.addr}: {pending}.")
            return

        try:
            #! Pretty important call.
            synchronizer.sync_input(pending)
            encoded = process_input(pending)
        except Exception as e:
            logger.error(f"Error when encoding data to {sender.addr}: {e}.", exc_info=True)
            return
    else:
        logger.debug(f"Sending leftovers from a previous command: {pending}.")
        encoded = pending

        try:
            sent_count = sender.send(encoded)
            logger.debug(f"Sent {sent_count} bytes to {sender.addr}")
        except BlockingIOError:
            logger.debug("Sending would block.")
            return
        except OSError as e:
            logger.error(f"Write error on {sender.addr}: {e}. Remove the sender if closed.")
            return
        
    if sent_count >= len(encoded):
        #! Pretty important call.
        synchronizer.all_sent = True
        sender.rem_first_pending()
        return

    # The command was not sent in one go.
    # Update the pending item with the remaining bytes.
    logger.debug(f"Partial send for {sender.addr}: {sent_count}/{len(encoded)} bytes sent.")
    remaining = encoded[sent_count:]
    sender.shrink_first_pending(remaining)

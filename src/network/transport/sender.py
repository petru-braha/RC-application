from collections import deque

from constants import EMPTY_LEN
from structs import Address
from util import process_input

from .sock import Sock

class Sender(Sock):
    """
    Handles buffering and sending commands to the socket.
    """
        
    def __init__(self, addr: Address) -> None:
        super().__init__(addr)
        self._pending_inputs = deque()

    def add_pending(self, pending: str) -> None:
        """
        Adds raw input string to the pending commands queue.

        Parameters:
            pending (str): The command to add.
        """
        self._pending_inputs.append(pending)

    def has_pending(self) -> bool:
        """
        Checks if there are pending commands to be sent.

        Returns:
            bool: True if there are pending commands, False otherwise.
        """
        return len(self._pending_inputs) > EMPTY_LEN

    def get_first_pending(self) -> str | None:
        """
        Retrieves the first pending command without removing it.

        Returns:
            str: The first pending command.
            None: If queue is empty.
        """
        if not self.has_pending():
            return None
        return self._pending_inputs[0]

    def rem_first_pending(self) -> bool:
        """
        Removes the first pending command from the queue.

        Returns:
            bool: True if a command was removed, False if queue was empty.
        """
        if not self.has_pending():
            return False
        self._pending_inputs.popleft()
        return True

    def send_first_pending(self) -> bool:
        """
        Sends data to the socket.
        Socket must be ready for writing!

        Sends and processes the first raw input appended to the deque.

        Returns:
            bool: True if the first was sent with success.

        Raises:
            BlockingIOError: If the socket is not ready for writing.
            OSError: If the socket is closed.
        """
        if not self.has_pending():
            return False
        
        pending = self.get_first_pending()
        assert pending != None
        
        # When partial send occurs,
        # the first pending input becomes the remaining bytes from the original call.
        if isinstance(pending, str):
            encoded = process_input(pending)
        else:
            encoded = pending
        
        try:
            sent_count = self._sock.send(encoded)
        except BlockingIOError:
            return False
        
        if sent_count >= len(encoded):
            # We will not pop the first pending input here.
            return True

        # The command was not sent in one go.
        # Update the pending item with the remaining bytes.
        remaining = encoded[sent_count:]
        self._pending_inputs[0] = remaining
        return True

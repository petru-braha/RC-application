from collections import deque

from constants import EMPTY_LEN
from structs import Address

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

    def get_first_pending(self) -> str | bytes | None:
        """
        Retrieves the first pending command without removing it.

        Returns:
            str: The first pending command.
            bytes: The encoded leftover of the first pending command.
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

    def shrink_first_pending(self, remaining: bytes) -> None:
        """
        Updates the first pending command with the remaining bytes after a partial send.

        Parameters:
            remaining (bytes): The bytes that were not sent.
        """
        assert self.has_pending()
        self._pending_inputs[0] = remaining

    def send(self, data: bytes) -> int:
        """
        Sends raw bytes to the socket.
        Socket must be ready for writing!

        Parameters:
            data (bytes): The data to send.

        Returns:
            int: The number of bytes sent.

        Raises:
            BlockingIOError: If the socket is not ready for writing.
            OSError: If the socket is closed.
        """
        return self._sock.send(data)

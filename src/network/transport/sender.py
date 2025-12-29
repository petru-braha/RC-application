from collections import deque

from constants import EMPTY_LEN
from structs import Address

from .sock import Sock

class Sender(Sock):
    """
    Handles buffering and sending commands to the socket.
    """

    _ASCII_ENC: str = "ascii"
    """
    "RESP is a binary protocol that uses control sequences encoded in standard ASCII."
    https://redis.io/docs/latest/develop/reference/protocol-spec/
    """
        
    def __init__(self, addr: Address) -> None:
        super().__init__(addr)
        self._pending_encoded_inputs = deque()

    def add_encoded(self, input_str: str) -> None:
        """
        Adds a command string to the pending commands queue.

        Parameters:
            input_str (str): The command to add.
        """
        self._pending_encoded_inputs.append(input_str)

    def has_pending(self) -> bool:
        """
        Checks if there are pending commands to be sent.

        Returns:
            bool: True if there are pending commands, False otherwise.
        """
        return len(self._pending_encoded_inputs) > EMPTY_LEN

    def get_first_pending(self) -> str | None:
        """
        Retrieves the first pending command without removing it.

        Returns:
            str: The first pending command.
            None: If queue is empty.
        """
        if not self._pending_encoded_inputs:
            return None
        return self._pending_encoded_inputs[0]

    def rem_first_pending(self) -> bool:
        """
        Removes the first pending command from the queue.

        Returns:
            bool: True if a command was removed, False if queue was empty.
        """
        if not self._pending_encoded_inputs:
            return False
        self._pending_encoded_inputs.popleft()
        return True

    def send_first_pending(self) -> bool:
        """
        Sends data to the socket.
        Socket must be ready for writing!

        Parameters:
            data (bytes): The data to send.

        Returns:
            bool: False if there was no pending commands,
                  True if the first was sent with success.

        Raises:
            BlockingIOError: If the socket is not ready for writing.
            OSError: If the socket is closed.
        """
        data = self.get_first_pending()
        if data == None:
            return False
        
        data = data.encode(Sender._ASCII_ENC)
        self._sock.sendall(data)
        return True

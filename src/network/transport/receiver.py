from protocol.constants_resp import CRLF

from constants import EMPTY_LEN
from exceptions import PartialResponseError
from structs import Address

from .sock import Sock

class Receiver(Sock):
    """
    Handles reading data from the socket and managing the output buffer.
    """
    
    _4KB_BUFSIZE: int = 4096
    """
    Default buffer size for read operations (4KB).
    """

    def __init__(self, addr: Address) -> None:
        super().__init__(addr)
        self._buf = bytearray()

    def empty_buf(self) -> bool:
        """
        Checks if the internal buffer is empty.

        Returns:
            bool: True if buffer is empty, False otherwise.
        """
        return len(self._buf) == EMPTY_LEN

    def consume(self, bufsize: int) -> str:
        """
        Consumes a specific number of bytes from the buffer.
        And coverts it into UTF-8 string.

        Parameters:
            bufsize (int): The number of bytes to consume.

        Returns:
            str: The consumed data as a string.
        
        Raises:
            PartialResponseError: If there are insufficient bytes in the buffer.
        """
        if bufsize > len(self._buf):
            raise PartialResponseError(f"Insufficient buffer bytes: {len(self._buf)}. Needed: {bufsize}")
        
        data = self._buf[:bufsize]
        del self._buf[:bufsize]
        return data.decode()

    def consume_crlf(self) -> str:
        """
        Consumes a line from the buffer, ending with CRLF.
        And coverts it into UTF-8 string.

        Returns:
            str: The consumed line as a string, including CRLF.
        
        Raises:
            PartialResponseError: If the buffer does not contain a CRLF.
        """
        ASCII_CRLF = CRLF.encode()
        try:
            idx = self._buf.index(ASCII_CRLF)
        except ValueError:
            raise PartialResponseError("Buffer does not contain a CRLF.")
        
        end_idx = idx + len(ASCII_CRLF)
        data = self._buf[:end_idx]
        del self._buf[:end_idx]
        return data.decode()

    def recv(self, bufsize: int = _4KB_BUFSIZE) -> int:
        """
        Reads data from the socket into the buffer.
        The socket must be ready for reading!

        Parameters:
            bufsize (int): The maximum number of bytes to read.

        Returns:
            int: The number of bytes read.

        Raises:
            BlockingIOError: If the socket is not ready for reading.
            OSError: If the socket is closed.
        """
        data = self._sock.recv(bufsize)
        self._buf.extend(data)
        return len(data)

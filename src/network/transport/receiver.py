from socket import socket

import core

from .interfaces import Communicator

logger = core.get_logger(__name__)

class Receiver(Communicator):
    """
    Performs buffered reads from the socket and manages the output buffer.
    """
    
    _4KB_BUFSIZE: int = 4096
    """
    Default buffer size for read operations (4KB).
    """

    def __init__(self, socket: socket) -> None:
        self._socket = socket
        self._buf = bytearray()
        self._idx = 0

    def empty_buf(self) -> bool:
        """
        Checks if the internal buffer is empty.

        Returns:
            bool: True if buffer is empty, False otherwise.
        """
        return self._idx >= len(self._buf)

    def consume(self, bufsize: int) -> str:
        """
        Consumes a specific number of bytes from the buffer.
        And coverts it into UTF-8 string.

        Args:
            bufsize (int): The number of bytes to consume.

        Returns:
            str: The consumed data as a string.
        
        Raises:
            PartialResponseError: If there are insufficient bytes in the buffer.
        """
        if self._idx + bufsize > len(self._buf):
            raise core.PartialResponseError(f"Insufficient buffer bytes: {len(self._buf) - self._idx}. Needed: {bufsize}")
        
        data = self._buf[self._idx : self._idx + bufsize]
        self._idx += bufsize
        
        logger.debug(f"Consumed {bufsize} bytes from buffer. Remaining: {len(self._buf) - self._idx}.")
        return data.decode()

    def consume_crlf(self) -> str:
        """
        Consumes a line from the buffer, ending with CRLF.
        And coverts it into UTF-8 string.

        Returns:
            str: The consumed line as a string, NOT including CRLF.
        
        Raises:
            PartialResponseError: If the buffer does not contain a CRLF.
        """
        ASCII_CRLF = core.CRLF.encode()
        try:
            # Search for CRLF starting from current index.
            end_idx = self._buf.index(ASCII_CRLF, self._idx)
        except ValueError:
            raise core.PartialResponseError("Buffer does not contain a CRLF")
        
        # Here we want to consume CRLF but not include it the returned string.
        data = self._buf[self._idx : end_idx]
        end_idx += len(ASCII_CRLF)
        
        logger.debug(f"Consumed {end_idx - self._idx} bytes from buffer. Remaining: {len(self._buf) - end_idx}.")
        self._idx = end_idx
        return data.decode()

    def restore_buf(self, idx: int) -> None:
        """
        Restores the buffer to the specified index.
        
        Args:
            idx (int): The index to restore the buffer to.
        
        Raises:
            ValueError: If the index is greater than the current index.
        """
        if idx > self._idx:
            raise ValueError("Cannot restore buffer to an index greater than the current index")
        
        logger.debug(f"Restore {self._idx - idx} bytes.")
        self._idx = idx

    def recv(self, bufsize: int = _4KB_BUFSIZE) -> int:
        """
        Reads data from the socket extending the buffer.

        Args:
            bufsize (int): The maximum number of bytes to read.

        Returns:
            int: The number of bytes read.

        Raises:
            BlockingIOError: If the socket is not ready for reading.
            ConnectionError: If the socket is closed by the peer.
        """
        data = self._socket.recv(bufsize)
        if len(data) == core.EMPTY_LEN:
            raise ConnectionError("Socket closed by peer")

        self._buf.extend(data)
        logger.debug(f"Received {len(data)} bytes from socket. Available: {len(self._buf) - self._idx}.")
        return len(data)
    
    def cleanup(self) -> None:
        """
        Discards the consumed part of the buffer.

        This call should be used when after a complete response is received.
        The buffer should be completely cleaned after this.

        Raises:
            AssertionError: If the buffer is not empty after cleanup.
        """
        self._buf = self._buf[self._idx:]
        self._idx = 0
        assert self.empty_buf()

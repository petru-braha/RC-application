import socket

from src.protocol.constants_resp import CRLF
from src.network import Sock

class Receiver:
    """
    Byte fetcher decoupled from the protocol algorithms.

    Allows buffered reads from sockets.
    """


    _sock_bufs: dict[Sock, bytearray] = {}

    @staticmethod
    def register(sock: Sock):
        Receiver._sock_bufs[sock] = bytearray()

    @staticmethod
    def unregister(sock: Sock):
        Receiver._sock_bufs.pop(sock, None)

    @staticmethod
    def recv(sock: Sock, encoded: str):
        """
        simple Connection.
        Actually called by
        """
        pass

    @staticmethod
    def handle_read(sock: Connection) -> bool:
        hist = AppState.sock_hist_dict[connection]

        for dialogue in hist:
            if dialogue.output == None:
                bytes = prepare_cmd(dialogue.cmd)
                connection.sendall(bytes)
                return True
        return False

    
    _4KB_BUFSIZE: int = 4096
    """
    Buffer size for receiving data.
    """

    def consume(self, bufsize: int) -> str:
        """
        Only consumes buffer.

        Returns:
            str: Data consumed.

        Raises:
            PartialResponseError: If the buffer size is greater than available data.
        """
        if bufsize > len(self._buf):
            raise PartialResponseError(f"Insufficient buffer bytes: {len(self._buf)}. Needed: {bufsize}")
        
        data = self._buf[:bufsize]
        del self._buf[:bufsize]
        return data.decode()

    def consume_crlf(self) -> str:
        """
        Only consumes buffer.
        Used by the decoder.

        Returns:
            str: Data consumed.

        Raises:
            PartialResponseError: If the buffer does not contain a CRLF.
        """
        sep = CRLF.encode()
        
        try:
            idx = self._buf.index(sep)
        except ValueError:
            raise PartialResponseError("Buffer does not contain a CRLF.")
        
        end_pos = idx + len(sep)
        data = self._buf[:end_pos]
        del self._buf[:end_pos]
        return data.decode()

    def recv(self) -> int:
        """
        Uses multiplexing to check for availability, then reads as much as possible.

        Returns:
            int: Number of bytes read.
        """
        readable, _, _ = select([self.sock], [], [], 0)
        if not readable:
            return 0
        
        try:
            data = self.sock.recv(bufsize, socket.MSG_DONTWAIT)
            self._buf.extend(data)
        except BlockingIOError:
            pass
        except OSError:
            pass
            
        return len(data)

    def has_leftovers(self) -> bool:
        """
        Returns:
            bool: True if there are leftovers in the buffer.
        """
        return len(self._buf) > 0

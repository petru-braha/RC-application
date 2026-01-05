import socket
import collections

from core import Config
from core.structs import Address

from .connection import Connection

logger = Config.get_logger(__name__)

class MockConnection(Connection):
    """
    Mock implementation of Connection for UI testing and simulation.
    Bypasses real network IO but maintains compatibility with Reactor's selector.
    """

    def __init__(self, host: str, port: str, user: str, pasw: str, db_idx: str) -> None:
        """
        Initializes a mock connection with a loopback socket pair.
        """
        logger.info(f"Initializing MOCK connection for {host}:{port}.")
        
        # Initialize attributes normally handled by parent classes
        self.addr = Address(host, port)
        self._pending_inputs = collections.deque()
        self._buf = bytearray()
        self._idx = 0
        self.initial_user = user
        self.initial_pasw = pasw

        # Create a socket pair to satisfy selectors.
        # self._socket is used by the application (Reactor/Receiver/Sender).
        # self._peer is used to simulate the server side.
        self._socket, self._peer = socket.socketpair()
        self._socket.setblocking(False)
        self._peer.setblocking(False)

    def send(self, data: bytes) -> int:
        """
        Intercepts data sent to the socket and queues a mock response.
        """
        logger.debug(f"[MOCK] Sending {len(data)} bytes: {data!r}")
        # Send to the peer socket so it appears in the buffer if we were reading it,
        # but here we just want to trigger a response.
        
        # Simple echo/ok simulation:
        # Write to _socket's peer so _socket becomes readable.
        response = b"+OK\r\n"
        try:
            self._peer.send(response)
        except BlockingIOError:
            pass # buffer full
            
        return len(data) # Pretend we sent everything

    def recv(self, bufsize: int = 4096) -> int:
        """
        Reads from the local socket pair (data pushed by our mock response logic).
        """
        return super().recv(bufsize)

    def close(self) -> None:
        logger.info("[MOCK] Closing connection.")
        self._socket.close()
        self._peer.close()

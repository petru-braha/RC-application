import selectors

# Avoid circular import by importing inside methods or using string type hints if possible
# But here we need isinstance check.
# The user moved Connection to src/network/connection.py
# Reactor is in src/core/reactor.py
# So we import from network
from network import Connection

from .specs import Specs
from .selector import Selector

class Reactor(Specs, Selector):
    """
    Event loop manager using the most efficient I/O multiplexing mechanism
    available on the system (epoll, kqueue, select, etc.).
    """

    @staticmethod
    def tick(timeout: float | None = None) -> None:
        """
        Polls for I/O events and dispatches them to the registered handlers.
        
        Args:
            timeout: The maximum time to wait for events. None to wait indefinitely.
        """
        events = Reactor._SELECTOR.select(timeout=timeout)
        for key, mask in events:
            
            conn = key.fileobj
            assert isinstance(conn, Connection)
            
            if mask & selectors.EVENT_READ:
                Reactor._handle_read(conn)
            if mask & selectors.EVENT_WRITE:
                Reactor._handle_write(conn)

    @staticmethod
    def _handle_read(conn: Connection) -> None:
        """
        Reads from the socket, decodes data, and updates history.
        """
        is_empty = conn.empty_buf()
        
        # 1. Read from socket to buffer
        bytes_read = conn.recv()
        
        # 2. Decode and Archive if we have data
        if not conn.empty_buf():
            # Simplistic decoding for now as per previous context
            try:
                # Example:
                # data = conn.consume_crlf()
                # conn.archive(...)
                pass
            except Exception:
                pass

    @staticmethod
    def _handle_write(conn: Connection) -> None:
        """
        Sends pending commands to the socket.
        """
        # 1. Get first pending command
        cmd = conn.get_pending_cmd()
        # Requirement: "you can not remove first pending - data needed for read"
        
        if cmd:
            # 2. Convert to bytes (RESP protocol encoding)
            # For now, just sending raw
            data = cmd.encode('ascii') 
            
            # 3. Send
            conn.send_data(data)
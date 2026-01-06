from core.structs import Address

from .transport import Receiver, Sender, Sock, Synchronizer

class Transmitter:
    """
    Base class for a connection.
    
    Contains all necessary modules for a reliable communication with the remote server.

    Attributes:
        receiver (obj): Receives data from the remote server.
        sender (obj): Sends data to the remote server.
        synchronizer (obj): Manages the state of receival and sending.
    """
    
    def __init__(self, addr: Address) -> None:
        self.sock = Sock(addr)
        self.receiver = Receiver(self.sock._socket)
        self.sender = Sender(self.sock._socket)
        self.synchronizer = Synchronizer()
    
    @property
    def addr(self) -> Address:
        return self.sock.addr

    def close(self) -> None:
        self.sock.close()
    
    def fileno(self) -> int:
        return self.sock.fileno()

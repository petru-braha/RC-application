import socket

from core.config import get_logger
from core.structs import Address

logger = get_logger(__name__)

class Sock:
    """
    Establishes a TCP connection to a Redis server instance.
    """
    
    _DEFAULT_OPT_VALUE: int = 1
    """
    Default integer value to enable socket options.
    """
    
    def __init__(self, addr: Address) -> None:
        """
        Iterates through the available address families (IPv4/IPv6) returned 
        by DNS resolution and attempts to connect to the first one available. 
        Configures the socket with KEEPALIVE and TCP_NODELAY
        for optimal performance.

        Parameters:
            addr (Address): The address (host, port) to connect to.

        Raises:
            ConnectionError: If DNS resolution fails or
                             no connection was established.
        """
        logger.debug(f"Resolving address for {addr}...")
        try:
            addr_infos = socket.getaddrinfo(
                addr.host, addr.port,
                socket.AF_UNSPEC,
                socket.SOCK_STREAM)
        except socket.gaierror as e:
            raise ConnectionError(
                f"Failed to resolve address {addr.host}:{addr.port}") from e

        for family, socktype, prot, _, sockaddr in addr_infos:
            sock = None
            try:
                sock = socket.socket(family, socktype, prot)
                # To detect if the server has crashed or disconnected.
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, Sock._DEFAULT_OPT_VALUE)
                # Disables Nagle's algorithm to ensure small latency.
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, Sock._DEFAULT_OPT_VALUE)
                
                logger.debug(f"Connecting to {sockaddr}...")
                sock.connect(sockaddr)
                # Enable multiplexing only after successful connection.
                sock.setblocking(False)
                logger.info(f"Successfully connected to {addr} ({sockaddr}).")
                break
            except (socket.error, InterruptedError) as e:
                logger.warning(f"Failed to connect to {sockaddr}: {e}.")
                if sock:
                    sock.close()
                sock = None

        if sock == None:
            # No address available.
            logger.error(f"Could not establish connection to {addr} after trying all address families.")
            raise ConnectionError(f"Failed to connect to {addr.host}:{addr.port}")
        
        # Initially, Sock was planned to inherit from socket.socket.
        # This can't be possible: "The newly created socket is non-inheritable".
        # https://docs.python.org/3/library/socket.html
        self._socket = sock
        self.addr = addr
        
    def close(self) -> None:
        """
        Gracefully shuts down and closes the TCP connection.

        Stops the socket's read/write channels to alert the Redis server,
        then releases the local socket resources.
        If the socket is already closed, the method returns silently.
        """
        if self._socket._closed:
            return
        
        logger.info(f"Closing connection to {self.addr}.")
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
        except OSError as e:
            # The socket might be broken or closed by the peer first.
            logger.debug(f"Error when shutting down {self.addr} (likely already closed): {e}.")
        finally:
            self._socket.close()

    def fileno(self) -> int:
        """
        Returns the file descriptor of the socket.
        """
        return self._socket.fileno()

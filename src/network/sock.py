import socket

from src.types import Address

class Sock(socket.socket):
    """
    Establishes a TCP connection to a Redis server instance.
    """

    def __init__(self, addr: Address) -> None:
        """
        Iterates through the available address families (IPv4/IPv6) returned 
        by DNS resolution and attempts to connect to the first one available. 
        Configures the socket with KEEPALIVE and TCP_NODELAY
        for optimal performance.

        Args:
            addr (Address): The address (host, port) to connect to.

        Raises:
            ConnectionError: If DNS resolution fails or
                             no connection was established.
        """
        try:
            addr_infos = socket.getaddrinfo(
                addr.host, addr.port,
                socket.AF_UNSPEC,
                socket.SOCK_STREAM)
        except socket.gaierror as e:
            raise ConnectionError(
                f"Failed to resolve address {addr.host}:{addr.port}.") from e

        for family, socktype, prot, _, sockaddr in addr_infos:
            try:
                super().__init__(family, socktype, prot)
                
                # To detect if the server has crashed or disconnected.
                self.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                # Disables Nagle's algorithm to ensure small latency.
                self.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                
                self.connect(sockaddr)
                self.setblocking(False)
                self.addr = addr
                return

            except socket.error as e:
                self.close()
                continue
        
        # No address available.
        raise ConnectionError(f"Failed to connect to {addr.host}:{addr.port}.")
    
    def try_close(self) -> None:
        """
        Gracefully shuts down and closes the TCP connection.

        Stops the socket's read/write channels to alert the Redis server,
        then releases the local socket resources.
        If the socket is already closed, the method returns silently.
        """
        if self._closed:
            return
        
        try:
            self.shutdown(socket.SHUT_RDWR)
        except OSError:
            # The socket might be broken or closed by the peer first.
            pass
        finally:
            self.close()

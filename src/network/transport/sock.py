import socket

from structs import Address

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
        try:
            addr_infos = socket.getaddrinfo(
                addr.host, addr.port,
                socket.AF_UNSPEC,
                socket.SOCK_STREAM)
        except socket.gaierror as e:
            raise ConnectionError(
                f"Failed to resolve address {addr.host}:{addr.port}.") from e

        for family, socktype, prot, _, sockaddr in addr_infos:
            sock = None
            try:
                sock = socket.socket(family, socktype, prot)
            except socket.error:
                if sock:
                    sock.close()

        if sock == None:
            # No address available.
            raise ConnectionError(f"Failed to connect to {addr.host}:{addr.port}.")
                
        # To detect if the server has crashed or disconnected.
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, Sock._DEFAULT_OPT_VALUE)
        # Disables Nagle's algorithm to ensure small latency.
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, Sock._DEFAULT_OPT_VALUE)
        # Enable multiplexing.
        sock.setblocking(False)
        
        try:
            sock.connect(sockaddr)
        except InterruptedError:
            pass
        # Initially, Sock was planned to inherit from socket.socket.
        # This can't be possible: "The newly created socket is non-inheritable".
        # https://docs.python.org/3/library/socket.html
        self._sock = sock
        self.addr = addr
        
    def close(self) -> None:
        """
        Gracefully shuts down and closes the TCP connection.

        Stops the socket's read/write channels to alert the Redis server,
        then releases the local socket resources.
        If the socket is already closed, the method returns silently.
        """
        if self._sock._closed:
            return
        
        try:
            self._sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            # The socket might be broken or closed by the peer first.
            pass
        finally:
            self._sock.close()

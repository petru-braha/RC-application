from unittest import TestCase
from unittest.mock import MagicMock, patch, call
import socket

from src.core.structs import Addr
from src.network.transport.sock import Sock

class TestSock(TestCase):
    
    socket_cls_patcher = patch("src.network.transport.sock.socket.socket")
    getaddrinfo_patcher = patch("src.network.transport.sock.socket.getaddrinfo")
    
    def setUp(self):
        self.host = "localhost"
        self.port = "6379"
        self.addr = Addr(self.host, self.port)
        self.sockaddr = (self.host, int(self.port))
        
        self.mock_socket_cls = TestSock.socket_cls_patcher.start()
        self.mock_getaddrinfo = TestSock.getaddrinfo_patcher.start()

    def tearDown(self):
        TestSock.socket_cls_patcher.stop()
        TestSock.getaddrinfo_patcher.stop()

    def test_init_success_ipv4(self):
        mock_socket_instance = MagicMock()
        self.mock_socket_cls.return_value = mock_socket_instance
        
        # Mock getaddrinfo to return one address (IPv4).
        self.mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", self.sockaddr)
        ]

        sock = Sock(self.addr)

        self.mock_getaddrinfo.assert_called_with(
            self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM
        )
        self.mock_socket_cls.assert_called_with(socket.AF_INET, socket.SOCK_STREAM, 6)
        
        # Verify socket configuration.
        mock_socket_instance.setsockopt.assert_has_calls([
            call(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
            call(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        ])
        
        mock_socket_instance.connect.assert_called_with(self.sockaddr)
        mock_socket_instance.setblocking.assert_called_with(False)
        
        self.assertEqual(sock._socket, mock_socket_instance)
        self.assertEqual(sock.addr, self.addr)

    def test_init_fail_all_families(self):
        """
        Mocks are set to fail connection on all attempts.
        """
        mock_socket_instance = MagicMock()
        self.mock_socket_cls.return_value = mock_socket_instance
        mock_socket_instance.connect.side_effect = socket.error("Connection refused")
        
        # Return two addresses to try.
        self.mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", self.sockaddr),
            (socket.AF_INET6, socket.SOCK_STREAM, 6, "", self.sockaddr)
        ]

        with self.assertRaises(ConnectionError) as cm:
            Sock(self.addr)
        
        self.assertIn(f"Failed to connect to {self.addr}", str(cm.exception))
        
        self.assertEqual(mock_socket_instance.connect.call_count, 2)
        self.assertEqual(mock_socket_instance.close.call_count, 2)

    def test_init_dns_failure(self):
        self.mock_getaddrinfo.side_effect = socket.gaierror("Name or service not known")
        
        with self.assertRaises(ConnectionError) as cm:
            Sock(self.addr)
            
        self.assertIn(f"Failed to resolve address {self.addr}", str(cm.exception))

    def test_close(self):
        mock_socket_instance = MagicMock()
        self.mock_socket_cls.return_value = mock_socket_instance
        self.mock_getaddrinfo.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", self.sockaddr)]
        
        sock = Sock(self.addr)
        
        mock_socket_instance._closed = False
        sock.close()
        
        mock_socket_instance.shutdown.assert_called_with(socket.SHUT_RDWR)
        mock_socket_instance.close.assert_called()

    def test_close_handle_oserror(self):
        mock_socket_instance = MagicMock()
        mock_socket_instance._closed = False
        mock_socket_instance.shutdown.side_effect = OSError("Socket not connected")
        
        self.mock_socket_cls.return_value = mock_socket_instance
        self.mock_getaddrinfo.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", self.sockaddr)]
        
        sock = Sock(self.addr)
        # Should not raise.
        sock.close()
        
        mock_socket_instance.close.assert_called()

    def test_close_already_closed(self):
        mock_socket_instance = MagicMock()
        mock_socket_instance._closed = True
        
        self.mock_socket_cls.return_value = mock_socket_instance
        self.mock_getaddrinfo.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", self.sockaddr)]
        
        sock = Sock(self.addr)
        sock.close()
        
        mock_socket_instance.shutdown.assert_not_called()

    def test_fileno(self):
        mock_socket_instance = MagicMock()
        self.mock_socket_cls.return_value = mock_socket_instance
        self.mock_getaddrinfo.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", self.sockaddr)]
        mock_socket_instance.fileno.return_value = 123
        
        sock = Sock(self.addr)
        self.assertEqual(sock.fileno(), 123)

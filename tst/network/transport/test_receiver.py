from unittest import TestCase
from unittest.mock import MagicMock

from core.exceptions import PartialResponseError
from src.core.constants import CRLF
from src.network.transport.receiver import Receiver

class TestReceiver(TestCase):
    
    def setUp(self):
        self.mock_socket = MagicMock()
        self.receiver = Receiver(self.mock_socket)

    def test_empty_buf(self):
        self.receiver._buf = bytearray(b"")
        self.receiver._idx = 0
        self.assertTrue(self.receiver.empty_buf())

        self.receiver._buf = bytearray(b"1")
        self.assertFalse(self.receiver.empty_buf())

    def test_recv_success(self):
        data = b"Hello"
        self.mock_socket.recv.return_value = data
        
        received = self.receiver.recv(10)
        
        self.mock_socket.recv.assert_called_with(10)
        self.assertEqual(received, len(data))
        self.assertEqual(self.receiver._buf, bytearray(data))

    def test_recv_socket_closed(self):
        self.mock_socket.recv.return_value = b""
        
        with self.assertRaises(ConnectionError):
            self.receiver.recv(10)

    def test_consume(self):
        self.receiver._buf = bytearray(b"Hello World")
        self.receiver._idx = 0
        
        data = self.receiver.consume(5)
        self.assertEqual(data, "Hello")
        self.assertEqual(self.receiver._idx, 5)
        
        data = self.receiver.consume(6)
        self.assertEqual(data, " World")
        self.assertEqual(self.receiver._idx, 11)

    def test_consume_insufficient_bytes(self):
        self.receiver._buf = bytearray(b"Hi")
        self.receiver._idx = 0
        
        with self.assertRaises(PartialResponseError):
            self.receiver.consume(5)

    def test_consume_crlf(self):
        self.receiver._buf = bytearray(b"Line1\r\nLine2")
        self.receiver._idx = 0
        
        line = self.receiver.consume_crlf()
        self.assertEqual(line, "Line1")
        # Index should be after \r\n (5 + 2 = 7).
        self.assertEqual(self.receiver._idx, 7)

    def test_consume_crlf_missing(self):
        self.receiver._buf = bytearray(b"Line1 without terminator")
        self.receiver._idx = 0
        
        with self.assertRaises(PartialResponseError):
            self.receiver.consume_crlf()

    def test_restore_buf(self):
        self.receiver._buf = bytearray(b"12345")
        self.receiver._idx = 3
        
        self.receiver.restore_buf(1)
        self.assertEqual(self.receiver._idx, 1)

    def test_restore_buf_invalid(self):
        """
        Test ValueError raising if the restoration index is greater than the current one.
        """
        self.receiver._buf = bytearray(b"12345")
        self.receiver._idx = 3
        
        with self.assertRaises(ValueError):
            self.receiver.restore_buf(4)

    def test_cleanup_success(self):
        self.receiver._buf = bytearray(b"Consumed")
        self.receiver._idx = 8
        self.receiver.cleanup()
        self.assertEqual(self.receiver._buf, bytearray(b""))
        self.assertEqual(self.receiver._idx, 0)
    
    def test_cleanup_error(self):
        self.receiver._buf = bytearray(b"ConsumedRemaining")
        # 8 bytes were consumed.
        self.receiver._idx = 8
        
        # Cleanup asserts that buffer should be empty after cleanup.
        # Since we have "Remaining", it should raise AssertionError.
        with self.assertRaises(AssertionError):
            self.receiver.cleanup()

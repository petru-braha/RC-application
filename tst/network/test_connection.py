from unittest import TestCase
from unittest.mock import MagicMock, patch

from core.exceptions import ConnectionCountError
from src.network.connection import Connection

class TestConnection(TestCase):
    
    def setUp(self):
        # Reset Connection count before each test.
        Connection.count = 0
        
        self.sock_patcher = patch("src.network.transmitter.Sock")
        self.receiver_patcher = patch("src.network.transmitter.Receiver")
        self.sender_patcher = patch("src.network.transmitter.Sender")
        self.sync_patcher = patch("src.network.transmitter.Synchronizer")
        
        self.mock_sock_cls = self.sock_patcher.start()
        self.mock_receiver_cls = self.receiver_patcher.start()
        self.mock_sender_cls = self.sender_patcher.start()
        self.mock_sync_cls = self.sync_patcher.start()
        
        self.mock_sender_instance = MagicMock()
        self.mock_sender_cls.return_value = self.mock_sender_instance
        
        self.mock_sock_instance = MagicMock()
        self.mock_sock_cls.return_value = self.mock_sock_instance

    def tearDown(self):
        self.sock_patcher.stop()
        self.receiver_patcher.stop()
        self.sender_patcher.stop()
        self.sync_patcher.stop()

    def test_init_success(self):
        Connection("localhost", "6379", "user", "pass", "0")
        
        self.assertEqual(Connection.count, 1)

    def test_init_limit_reached(self):
        with patch("src.network.connection.MAX_CONNECTIONS", 1):
            Connection("localhost", "6379", "user", "pass", "0")
            self.assertEqual(Connection.count, 1)
            
            try:
                Connection("localhost", "6379", "user", "pass", "0")
                self.fail("ConnectionCountError not raised")
            except ConnectionCountError:
                pass
            
            # Count should remain 1.
            self.assertEqual(Connection.count, 1)

    def test_close(self):
        conn = Connection("localhost", "6379", "user", "pass", "0")
        self.assertEqual(Connection.count, 1)
        
        conn.close()
        
        self.assertEqual(Connection.count, 0)
        self.mock_sock_instance.close.assert_called()

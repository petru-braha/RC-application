from unittest import TestCase
from unittest.mock import MagicMock, patch

from core.structs import Address
from src.network.transmitter import Transmitter

class TestTransmitter(TestCase):
    
    def setUp(self):
        self.addr = Address("localhost", "6379")
        
        self.sock_patcher = patch("src.network.transmitter.Sock")
        self.receiver_patcher = patch("src.network.transmitter.Receiver")
        self.sender_patcher = patch("src.network.transmitter.Sender")
        self.sync_patcher = patch("src.network.transmitter.Synchronizer")
        
        self.mock_sock_cls = self.sock_patcher.start()
        self.mock_receiver_cls = self.receiver_patcher.start()
        self.mock_sender_cls = self.sender_patcher.start()
        self.mock_sync_cls = self.sync_patcher.start()

    def tearDown(self):
        self.sock_patcher.stop()
        self.receiver_patcher.stop()
        self.sender_patcher.stop()
        self.sync_patcher.stop()

    def test_init(self):
        mock_sock_instance = MagicMock()
        self.mock_sock_cls.return_value = mock_sock_instance
        
        transmitter = Transmitter(self.addr)
        
        self.mock_sock_cls.assert_called_with(self.addr)
        self.mock_receiver_cls.assert_called_with(mock_sock_instance._socket)
        self.mock_sender_cls.assert_called_with(mock_sock_instance._socket)
        self.mock_sync_cls.assert_called()
        
        self.assertEqual(transmitter.sock, mock_sock_instance)

    def test_delegations(self):
        mock_sock_instance = MagicMock()
        self.mock_sock_cls.return_value = mock_sock_instance
        mock_sock_instance.fileno.return_value = 10
        mock_sock_instance.addr = self.addr
        
        transmitter = Transmitter(self.addr)
        
        transmitter.close()
        mock_sock_instance.close.assert_called()
        
        self.assertEqual(transmitter.fileno(), 10)
        self.assertEqual(transmitter.addr, self.addr)

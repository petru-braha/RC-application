from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.core.structs import Addr
from src.network.transmitter import Transmitter

class TestTransmitter(TestCase):
    
    sock_patcher = patch("src.network.transmitter.Sock")
    receiver_patcher = patch("src.network.transmitter.Receiver")
    sender_patcher = patch("src.network.transmitter.Sender")
    sync_patcher = patch("src.network.transmitter.Synchronizer")

    def setUp(self):
        self.addr = Addr("localhost", "6379")
        
        self.mock_sock_cls = TestTransmitter.sock_patcher.start()
        self.mock_receiver_cls = TestTransmitter.receiver_patcher.start()
        self.mock_sender_cls = TestTransmitter.sender_patcher.start()
        self.mock_sync_cls = TestTransmitter.sync_patcher.start()

    def tearDown(self):
        TestTransmitter.sock_patcher.stop()
        TestTransmitter.receiver_patcher.stop()
        TestTransmitter.sender_patcher.stop()
        TestTransmitter.sync_patcher.stop()

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

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core.structs import Address
from src.network.identification import Identification

class TestIdentification(TestCase):
    
    def setUp(self):
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
        
        self.mock_sock_instance = self.mock_sock_cls.return_value
        self.mock_sock_instance.addr = Address("localhost", "6379")

    def tearDown(self):
        self.sock_patcher.stop()
        self.receiver_patcher.stop()
        self.sender_patcher.stop()
        self.sync_patcher.stop()

    def test_init_defaults(self):
        identification = Identification("", "", "", "")
        
        self.assertEqual(identification.addr, Address("localhost", "6379"))
        self.assertEqual(identification.initial_user, "default")
        self.assertEqual(identification.initial_pasw, "")
        
        expected_hello = "HELLO 3 AUTH default"
        self.mock_sender_instance.add_pending.assert_called_with(expected_hello)

    def test_init_custom(self):
        self.mock_sock_instance.addr = Address("127.0.0.1", "1234")
        identification = Identification("127.0.0.1", "1234", "user", "pass")
        
        self.assertEqual(identification.addr, Address("127.0.0.1", "1234"))
        self.assertEqual(identification.initial_user, "user")
        self.assertEqual(identification.initial_pasw, "pass")
        
        expected_hello = "HELLO 3 AUTH user pass"
        self.mock_sender_instance.add_pending.assert_called_with(expected_hello)

    def test_say_hello_custom_protocol(self):
        identification = Identification("localhost", "6379", "user", "pass")
        # Reset the default say_hello call that is perfomed at initialization.
        self.mock_sender_instance.reset_mock()
        
        identification.say_hello("user", "pass", protver=2)
        
        expected_hello = "HELLO 2 AUTH user pass"
        self.mock_sender_instance.add_pending.assert_called_with(expected_hello)

    def test_say_hello_invalid_protocol(self):
        identification = Identification("localhost", "6379", "user", "pass")
        # Reset the default say_hello call that is perfomed at initialization.
        self.mock_sender_instance.reset_mock()
        
        inputs = [0.1, -6, 99999, 256]
        for protver in inputs:
            with self.assertRaises(ValueError):
                identification.say_hello("user", "pass", protver=protver)
        
        self.mock_sender_instance.add_pending.assert_not_called()

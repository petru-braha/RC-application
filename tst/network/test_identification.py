from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.core.structs import Addr
from src.network.identification import Identification

class TestIdentification(TestCase):
    
    sock_patcher = patch("src.network.transmitter.Sock")
    receiver_patcher = patch("src.network.transmitter.Receiver")
    sender_patcher = patch("src.network.transmitter.Sender")
    sync_patcher = patch("src.network.transmitter.Synchronizer")
    
    def setUp(self):
        self.mock_sock_cls = TestIdentification.sock_patcher.start()
        self.mock_receiver_cls = TestIdentification.receiver_patcher.start()
        self.mock_sender_cls = TestIdentification.sender_patcher.start()
        self.mock_sync_cls = TestIdentification.sync_patcher.start()
        
        self.mock_sender_instance = MagicMock()
        self.mock_sender_cls.return_value = self.mock_sender_instance
        
        self.mock_sock_instance = self.mock_sock_cls.return_value
        self.mock_sock_instance.addr = Addr("localhost", "6379")

    def tearDown(self):
        TestIdentification.sock_patcher.stop()
        TestIdentification.receiver_patcher.stop()
        TestIdentification.sender_patcher.stop()
        TestIdentification.sync_patcher.stop()

    def test_init_defaults(self):
        identification = Identification("", "", "", "")
        
        self.assertEqual(identification.addr, Addr("localhost", "6379"))
        self.assertEqual(identification.initial_user, "default")
        self.assertEqual(identification.initial_pasw, "")
        
        expected_hello = "HELLO 3 AUTH default"
        self.mock_sender_instance.add_pending.assert_called_with(expected_hello)

    def test_init_custom(self):
        self.mock_sock_instance.addr = Addr("127.0.0.1", "1234")
        identification = Identification("127.0.0.1", "1234", "user", "pass")
        
        self.assertEqual(identification.addr, Addr("127.0.0.1", "1234"))
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

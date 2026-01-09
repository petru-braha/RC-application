from unittest import TestCase
from unittest.mock import MagicMock

from src.network.transport.sender import Sender

class TestSender(TestCase):
    
    def setUp(self):
        self.mock_socket = MagicMock()
        self.sender = Sender(self.mock_socket)

    def test_add_and_has_pending(self):
        self.assertFalse(self.sender.has_pending())
        
        self.sender.add_pending("LPUSH mylist carrot")
        self.assertTrue(self.sender.has_pending())

    def test_get_first_pending(self):
        self.assertIsNone(self.sender.get_first_pending())
        
        self.sender.add_pending("SET key 1")
        self.sender.add_pending("APPEND key 5")
        self.sender.add_pending("DECR key")
        
        self.assertEqual(self.sender.get_first_pending(), "SET key 1")

    def test_rem_first_pending(self):
        self.sender.add_pending("SADD myset value")
        self.sender.add_pending("SISMEMBER myset value")
        
        self.sender.rem_first_pending()
        self.assertEqual(self.sender.get_first_pending(), "SISMEMBER myset value")
        
        self.sender.rem_first_pending()
        self.assertFalse(self.sender.has_pending())
        
        with self.assertRaises(AssertionError):
            self.sender.rem_first_pending()

    def test_shrink_first_pending(self):
        self.sender.add_pending("HMSET myhash field1 value1 field2 value2")
        
        self.sender.shrink_first_pending(b"field2 value2")
        self.assertEqual(self.sender.get_first_pending(), b"field2 value2")
         
        self.sender.rem_first_pending()
        with self.assertRaises(AssertionError):
            self.sender.rem_first_pending()

    def test_send(self):
        data = b"ZADD myzset 5 member"
        self.mock_socket.send.return_value = len(data)
        
        sent = self.sender.send(data)
        
        self.mock_socket.send.assert_called_with(data)
        self.assertEqual(sent, len(data))

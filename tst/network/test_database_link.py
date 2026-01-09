from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.network.database_link import DatabaseLink

class TestDatabaseLink(TestCase):
    
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

    def tearDown(self):
        self.sock_patcher.stop()
        self.receiver_patcher.stop()
        self.sender_patcher.stop()
        self.sync_patcher.stop()

    def test_init_default_db(self):
        # 0 is default logical database, so no SELECT command should be sent.
        DatabaseLink("localhost", "6379", "user", "pass", "0")
        
        for call_args in self.mock_sender_instance.add_pending.call_args_list:
            self.assertNotIn("SELECT", call_args[0][0])

    def test_init_custom_db(self):
        DatabaseLink("localhost", "6379", "user", "pass", "1")
        
        self.mock_sender_instance.add_pending.assert_any_call("SELECT 1")

    def test_init_empty_db_string(self):
        # If db_idx is empty string, skip SELECT command.
        DatabaseLink("localhost", "6379", "user", "pass", "")
        
        for call_args in self.mock_sender_instance.add_pending.call_args_list:
            self.assertNotIn("SELECT", call_args[0][0])

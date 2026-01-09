from unittest import TestCase
from src.network.transport.synchronizer import Synchronizer

class TestSynchronizer(TestCase):
    
    def setUp(self):
        self.sync = Synchronizer()

    def test_initial_state(self):
        self.assertIsNone(self.sync.last_raw_input)
        self.assertIsNone(self.sync.all_sent)
        self.assertIsNone(self.sync.all_recv)

    def test_sync_input(self):
        cmd = "GET key"
        self.sync.sync_input(cmd)
        
        self.assertEqual(self.sync.last_raw_input, cmd)
        self.assertFalse(self.sync.all_sent)
        self.assertFalse(self.sync.all_recv)

    def test_unsync(self):
        self.sync.sync_input("CMD")
        self.sync.unsync()
        
        self.assertIsNone(self.sync.last_raw_input)
        self.assertIsNone(self.sync.all_sent)
        self.assertIsNone(self.sync.all_recv)

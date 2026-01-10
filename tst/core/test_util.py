from unittest import TestCase
import logging

from src.core.exceptions import AssignmentError
from src.core.util import LogCompressor, Immutable

class TestUtil(TestCase):

    # ------------------------------
    # ---- LogCompressor class -----
    # ------------------------------
    
    def test_valid_log_compressor_init(self):
        compressor = LogCompressor(max_bytes=10)
        self.assertEqual(compressor.max_bytes, 10)
    
    def test_invalid_log_compressor_init(self):
        with self.assertRaises(ValueError):
            LogCompressor(max_bytes=2)

    def test_log_compressor_format(self):
        """Test LogCompressor formatting and truncation."""
        
        # Case 1: Message shorter than max_bytes
        compressor = LogCompressor(max_bytes=10)
        record = logging.LogRecord("name", logging.INFO, "pathname", 1, "Short", (), None)
        compressor.format(record)
        self.assertEqual(record.msg, "Short")
        
        # Case 2: Message longer than max_bytes.
        # "Hello World" is 11 bytes. max_bytes=10. Suffix is "...".
        # Expect: "Hello W..." (7 bytes prefix + 3 bytes suffix = 10 bytes).
        compressor = LogCompressor(max_bytes=10)
        record = logging.LogRecord("name", logging.INFO, "pathname", 1, "Hello World", (), None)
        compressor.format(record)
        
        self.assertEqual(len(record.msg), 10)
        self.assertTrue(record.msg.endswith("..."))
        self.assertEqual(record.msg, "Hello W...")
        self.assertEqual(record.args, ())

        # Case 3: Message exactly max_bytes
        # "1234567890" (10 bytes)
        record = logging.LogRecord("name", logging.INFO, "pathname", 1, "1234567890", (), None)
        compressor.format(record)
        self.assertEqual(record.msg, "1234567890")
    
    # ------------------------------
    # ------ Immutable class -------
    # ------------------------------
    
    class TestObject(Immutable):
        def __init__(self, key: str, value: int):
            self.key = key
            self.value = value

    def test_initialization_success(self):
        obj = TestUtil.TestObject("test", 0)
        self.assertEqual(obj.key, "test")
        self.assertEqual(obj.value, 0)
        
    def test_assignment_failure(self):
        obj = TestUtil.TestObject("test", 1)
        with self.assertRaises(AssignmentError):
            obj.key = "cool"
        with self.assertRaises(AssignmentError):
            obj.value = 1

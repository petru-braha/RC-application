from unittest import TestCase

from src.core.exceptions import AssignmentError
from src.core.util import LogCompressor, Immutable

class TestUtil(TestCase):

    def test_log_compressor(self):
        pass

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

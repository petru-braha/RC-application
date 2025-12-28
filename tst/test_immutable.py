from unittest import TestCase

from exceptions import AssignmentError
from util import Immutable

class TestImmutable(TestCase):

    class TestObject(Immutable):
        def __init__(self, key: str, value: int):
            self.key = key
            self.value = value

    def test_initialization_success(self):
        obj = TestImmutable.TestObject("test", 0)
        self.assertEqual(obj.key, "test")
        self.assertEqual(obj.value, 0)
        
    def test_assignment_failure(self):
        obj = TestImmutable.TestObject("test", 1)
        with self.assertRaises(AssignmentError):
            obj.key = "cool"
        with self.assertRaises(AssignmentError):
            obj.value = 1

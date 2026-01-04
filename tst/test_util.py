from unittest import TestCase

from src.core.exceptions import AssignmentError
from src.util import process_redis_url

class TestUtil(TestCase):
    # ------------------------------
    # ---- process_input method ----
    # ------------------------------

    def test_process_input(self):
        expected = "test"
        actual = process_input("test")
        self.assertEqual(actual, expected)
        self.assertCalled(encoder, once)
        self.assertCalled(parser, once)

    # ------------------------------
    # -- process_redis_url method --
    # ------------------------------

    # format: redis[s]://[[username][:password]@][host][:port][/db-number]
    def test_process_simple_url(self):
        expected = ("localhost", "6379", "", "", "")
        actual = process_redis_url("redis://localhost:6379")
        self.assertEqual(actual, expected)

    def test_process_complete_url(self):
        expected = ("localhost", "6379", "petru", "cool_petru", "4")
        actual = process_redis_url("rediss://petru:cool_petru@localhost:6379/4")
        self.assertEqual(actual, expected)

    def test_process_empty_url(self):
        expected = ("", "", "", "", "")
        actual = process_redis_url("redis://")
        self.assertEqual(actual, expected)
    
    def test_process_url_invalid_scheme(self):
        with self.assertRaises(ValueError):
            process_redis_url("rEdIs://localhost:6379")
    
    def test_process_url_invalid_db(self):
        with self.assertRaises(ValueError):
            process_redis_url("redis://localhost:6379/my_db")

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

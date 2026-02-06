from unittest import TestCase
from unittest.mock import MagicMock

from src.core.exceptions import AssignmentError
from src.core.util import Immutable, uninterruptible, process_redis_url

class TestUtil(TestCase):
    
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

    # ------------------------------
    # - uninterruptible decorator --
    # ------------------------------

    def test_uninterruptible_success(self):
        func = MagicMock(return_value="OK")
        decorated = uninterruptible(func)
        result = decorated("arg")
        self.assertEqual(result, "OK")
        func.assert_called_with("arg")

    def test_uninterruptible_retry_on_interrupt(self):
        func = MagicMock(side_effect=[KeyboardInterrupt, SystemExit, GeneratorExit, "OK"])
        func.__name__ = "mock_func"
        
        decorated = uninterruptible(func)
        result = decorated("arg")
        
        self.assertEqual(result, "OK")
        self.assertEqual(func.call_count, 4)
        
    def test_uninterruptible_exception(self):
        func = MagicMock(side_effect=ValueError("fail"))
        decorated = uninterruptible(func)
        with self.assertRaises(ValueError):
            decorated("arg")
        self.assertEqual(func.call_count, 1)

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
            process_redis_url("red://localhost:6379")
    
    def test_raise_when_tls_enforced(self):
        with self.assertRaises(ValueError):
            process_redis_url("redis://localhost:6379", tls_enforced=True)
    
    def test_process_url_invalid_db(self):
        with self.assertRaises(ValueError):
            process_redis_url("redis://localhost:6379/my_db")

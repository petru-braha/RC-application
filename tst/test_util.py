from unittest import TestCase

from src.util import process_input, process_redis_url

class TestUtil(TestCase):
    # ------------------------------
    # ---- process_input method ----
    # ------------------------------

    def test_process_input(self):
        pass
        #expected = "test"
        #actual = process_input("test")
        #sself.assertEqual(actual, expected)

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
    
    def test_process_url_invalid_db(self):
        with self.assertRaises(ValueError):
            process_redis_url("redis://localhost:6379/my_db")

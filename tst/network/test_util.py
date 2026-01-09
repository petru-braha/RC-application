from unittest import TestCase

from src.network.util import join_cmd_argv

class TestUtil(TestCase):
    """
    Test cases for the util module of the network package.
    """
    
    # ------------------------------
    # ---- join_cmd_argv method ----
    # ------------------------------

    def test_simple_join(self):
        expected = "SET key 1"
        actual = join_cmd_argv("SET", ["key", "1"])
        self.assertEqual(actual, expected)

    def test_join_empty_argv(self):
        expected = "HELLO"
        actual = join_cmd_argv("HELLO", [])
        self.assertEqual(actual, expected)

    def test_join_empty_cmd(self):
        with self.assertRaises(ValueError):
            join_cmd_argv("", [])

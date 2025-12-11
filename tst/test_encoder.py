from unittest import TestCase
from src.protocol.encoder import encoder

class TestEncoder(TestCase):
    """
    We test the encoder only.
    Input validation is done within the sanitizer module.
    """

    def test_no_args(self):
        actual = encoder("PING", [])
        expected = (
            "*1\r\n"
            "$4\r\nPING\r\n"
        )
        self.assertEqual(actual, expected)

    def test_single_arg(self):
        actual = encoder("GET", ["mykey"])
        expected = (
            "*2\r\n"
            "$3\r\nGET\r\n"
            "$5\r\nmykey\r\n"
        )
        self.assertEqual(actual, expected)

    def test_multiple_args(self):
        argv = ["key", "field1", "value1"]
        actual = encoder("HSET", argv)
        expected = (
            "*4\r\n"
            "$4\r\nHSET\r\n"
            "$3\r\nkey\r\n"
            "$6\r\nfield1\r\n"
            "$6\r\nvalue1\r\n"
        )
        self.assertEqual(actual, expected)

    def test_empty_string_arg(self):
        """
        A valid RESP bulk string can have length 0.
        """
        actual = encoder("SET", ["key", ""])
        expected = (
            "*3\r\n"
            "$3\r\nSET\r\n"
            "$3\r\nkey\r\n"
            "$0\r\n\r\n"
        )
        self.assertEqual(actual, expected)

    def test_special_chars_arg(self):
        """
        Ensures escape chars inside arguments are handled literally.
        """
        actual = encoder("ECHO", ["hello\nworld"])
        expected = (
            "*2\r\n"
            "$4\r\nECHO\r\n"
            "$11\r\nhello\nworld\r\n"
        )
        self.assertEqual(actual, expected)

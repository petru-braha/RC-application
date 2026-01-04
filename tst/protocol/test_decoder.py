from frozendict import frozendict
from unittest import TestCase

from src.core.exceptions import PartialResponseError

from src.protocol.constants_resp import NULL
from src.protocol.decoder import decoder
from src.protocol.output import OutputStr, OutputErr, OutputSeq, OutputMap, OutputAtt

class MockReceiver:
    """
    Simulates the Receiver class for testing the decoder.
    Operates on string data directly to mimic the decoded output of a real Receiver.
    """
    def __init__(self, data: str):
        self.data = data
        self.idx = 0

    def consume(self, n: int) -> str:
        if self.idx + n > len(self.data):
             raise PartialResponseError(f"Insufficient buffer bytes. Needed {n}, has {len(self.data) - self.idx}")
        res = self.data[self.idx : self.idx + n]
        self.idx += n
        return res

    def consume_crlf(self) -> str:
        try:
            end = self.data.index('\r\n', self.idx)
        except ValueError:
             raise PartialResponseError("Buffer does not contain a CRLF")
        res = self.data[self.idx : end]
        self.idx = end + 2
        return res

class MockReceiver:
    """
    Simulates the Receiver class for testing the decoder.
    Operates on string data directly to mimic the decoded output of a real Receiver.
    """
    def __init__(self, data: str):
        self.data = data
        self.idx = 0

    def consume(self, n: int) -> str:
        if self.idx + n > len(self.data):
             raise PartialResponseError(f"Insufficient buffer bytes. Needed {n}, has {len(self.data) - self.idx}")
        res = self.data[self.idx : self.idx + n]
        self.idx += n
        return res

    def consume_crlf(self) -> str:
        try:
            end = self.data.index('\r\n', self.idx)
        except ValueError:
             raise PartialResponseError("Buffer does not contain a CRLF.")
        res = self.data[self.idx : end]
        self.idx = end + 2
        return res

class TestDecoder(TestCase):
    
    # ------------------------------
    # -------- Simple Types --------
    # ------------------------------

    def test_simple_string(self):
        receiver = MockReceiver("+OK\r\n")
        actual = decoder(receiver)
        expected = OutputStr("OK")
        self.assertEqual(actual, expected)

    def test_integer(self):
        receiver = MockReceiver(":1000\r\n")
        actual = decoder(receiver)
        expected = OutputStr("1000")
        self.assertEqual(actual, expected)

    def test_boolean(self):
        receiver = MockReceiver("#t\r\n")
        actual = decoder(receiver)
        expected = OutputStr("t")
        self.assertEqual(actual, expected)

    def test_double(self):
        receiver = MockReceiver(",1.23\r\n")
        actual = decoder(receiver)
        expected = OutputStr("1.23")
        self.assertEqual(actual, expected)

    def test_big_number(self):
        receiver = MockReceiver("(3492890328409238509324850943850943825024385\r\n")
        actual = decoder(receiver)
        expected = OutputStr("3492890328409238509324850943850943825024385")
        self.assertEqual(actual, expected)

    def test_simple_error(self):
        receiver = MockReceiver("-ERR unknown command\r\n")
        actual = decoder(receiver)
        expected = OutputErr("ERR unknown command")
        self.assertEqual(actual, expected)

    # ------------------------------
    # --------- Bulk Types ---------
    # ------------------------------

    def test_bulk_string_basic(self):
        receiver = MockReceiver("$6\r\nfoobar\r\n")
        actual = decoder(receiver)
        expected = OutputStr("foobar")
        self.assertEqual(actual, expected)

    def test_bulk_string_empty(self):
        receiver = MockReceiver("$0\r\n\r\n")
        actual = decoder(receiver)
        expected = OutputStr("")
        self.assertEqual(actual, expected)

    def test_bulk_string_null(self):
        receiver = MockReceiver("$-1\r\n")
        actual = decoder(receiver)
        expected = OutputStr(NULL)
        self.assertEqual(actual, expected)

    def test_resp3_null(self):
        receiver = MockReceiver("_\r\n")
        actual = decoder(receiver)
        expected = OutputStr(NULL)
        self.assertEqual(actual, expected)

    def test_bulk_error(self):
        receiver = MockReceiver("!21\r\nSYNTAX invalid syntax\r\n")
        actual = decoder(receiver)
        expected = OutputErr("SYNTAX invalid syntax")
        self.assertEqual(actual, expected)

    def test_verbatim_string(self):
        """
        The decoder strips the first 4 bytes (encoding + ":" of the content).
        """
        # Length 16: "txt:Some content" -> 3 (txt) + 1 (:) + 12 (content) = 16
        receiver = MockReceiver("=16\r\ntxt:Some content\r\n")
        actual = decoder(receiver)
        expected = OutputStr("Some content")
        self.assertEqual(actual, expected)

    # ------------------------------
    # --- Simple Aggregate Types ---
    # ------------------------------

    def test_array_flat(self):
        """No recursive structure test."""
        receiver = MockReceiver("*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n")
        actual = decoder(receiver)
        # Using Tuple
        expected = OutputSeq((
            OutputStr("foo"),
            OutputStr("bar")
        ))
        self.assertEqual(actual, expected)

    def test_map_flat(self):
        """No recursive structure test."""
        receiver = MockReceiver("%1\r\n+first\r\n:1\r\n")
        actual = decoder(receiver)
        # Using frozendict
        expected = OutputMap(frozendict({
            OutputStr("first"): OutputStr("1")
        }))
        self.assertEqual(actual, expected)

    def test_set_flat(self):
        receiver = MockReceiver("~2\r\n+a\r\n+b\r\n")
        actual = decoder(receiver)
        expected = OutputSeq((
            OutputStr("a"),
            OutputStr("b")
        ))
        self.assertEqual(actual, expected)

    def test_push(self):
        receiver = MockReceiver(">3\r\n+pubsub\r\n+channel1\r\n+msg1\r\n")
        actual = decoder(receiver)
        expected = OutputSeq((
            OutputStr("pubsub"),
            OutputStr("channel1"),
            OutputStr("msg1")
        ))
        self.assertEqual(actual, expected)

    # ------------------------------
    # - Recursive Aggregate Types --
    # ------------------------------

    def test_recursive_nested_array(self):
        """
        Structure: [ "Level1", [ "Level2", [ "Level3" ] ] ].
        """
        receiver = MockReceiver(
            "*2\r\n"
            "+Level1\r\n"
            "*2\r\n"
            "+Level2\r\n"
            "*1\r\n"
            "+Level3\r\n"
        )
        actual = decoder(receiver)
        
        expected = OutputSeq((
            OutputStr("Level1"),
            OutputSeq((
                OutputStr("Level2"),
                OutputSeq((
                    OutputStr("Level3"),
                ))
            ))
        ))
        self.assertEqual(actual, expected)

    def test_recursive_map_in_array(self):
        """
        Structure: [ "Meta", { "Key": "Value" } ].
        """
        receiver = MockReceiver(
            "*2\r\n"
            "+Meta\r\n"
            "%1\r\n"
            "+Key\r\n"
            "+Value\r\n"
        )
        actual = decoder(receiver)
        
        expected = OutputSeq((
            OutputStr("Meta"),
            OutputMap(frozendict({
                OutputStr("Key"): OutputStr("Value")
            }))
        ))
        self.assertEqual(actual, expected)

    def test_recursive_array_in_map(self):
        """
        Structure: { "ListKey": [1, 2] }.
        """
        receiver = MockReceiver(
            "%1\r\n"
            "+ListKey\r\n"
            "*2\r\n"
            ":1\r\n"
            ":2\r\n"
        )
        actual = decoder(receiver)

        # Frozendict containing a Tuple
        expected = OutputMap(frozendict({
            OutputStr("ListKey"): OutputSeq((
                OutputStr("1"),
                OutputStr("2")
            ))
        }))
        self.assertEqual(actual, expected)

    # ------------------------------
    # --- Complex Attribute Test ---
    # ------------------------------

    def test_complex_attributes(self):
        """
        Structure: |1 {source-command: 'GET'} *2 [ %2 {id: 1024, addr: ...}, %2 {id: 1025, addr: ...} ].
        """
        receiver = MockReceiver(
            "|1\r\n"
            "+source-command\r\n"
            "+DEBUG CLIENTS\r\n"
            "*2\r\n"
              "%2\r\n"
                "+id\r\n"
                ":1024\r\n"
                "+addr\r\n"
                "$15\r\n127.0.0.1:54321\r\n"
              "%2\r\n"
                "+id\r\n"
                ":1025\r\n"
                "+addr\r\n"
                "$15\r\n127.0.0.1:54322\r\n"
        )
        actual = decoder(receiver)

        expected_attributes = OutputMap(frozendict({
            OutputStr('source-command'): OutputStr('DEBUG CLIENTS')
        }))
        expected_payload = OutputSeq((
            OutputMap(frozendict({
                OutputStr('id'): OutputStr('1024'),
                OutputStr('addr'): OutputStr('127.0.0.1:54321')
            })),
            OutputMap(frozendict({
                OutputStr('id'): OutputStr('1025'),
                OutputStr('addr'): OutputStr('127.0.0.1:54322')
            }))
        ))
        expected = OutputAtt(expected_attributes, expected_payload)
        
        self.assertEqual(actual, expected)

    # ------------------------------
    # --------- Exceptions ---------
    # ------------------------------
    
    def test_invalid_start_byte(self):
        receiver = MockReceiver("?INVALID\r\n")

        with self.assertRaises(KeyError):
            decoder(receiver)

    def test_partial_consume(self):
        """
        Sends a bulk string length of 10, but provides less data.
        """
        receiver = MockReceiver("$10\r\nTooShort")
        with self.assertRaises(PartialResponseError):
            decoder(receiver)

    def test_partial_crlf(self):
        """
        Sends a simple string without CRLF.
        """
        receiver = MockReceiver("+NotFinished")
        with self.assertRaises(PartialResponseError):
            decoder(receiver)

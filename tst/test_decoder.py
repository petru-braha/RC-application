from unittest import TestCase
from frozendict import frozendict

from src.protocol.constants_resp import NULL
from src.protocol.decoder import decoder
from src.protocol.output import OutputStr, OutputSeq, OutputMap, OutputAtt

class TestDecoder(TestCase):
    
    # ------------------------------
    # -------- Simple Types --------
    # ------------------------------

    def test_simple_string(self):
        resp_input = "+OK\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("OK")
        self.assertEqual(actual, expected)

    def test_integer(self):
        resp_input = ":1000\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("1000")
        self.assertEqual(actual, expected)

    def test_boolean(self):
        resp_input = "#t\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("t")
        self.assertEqual(actual, expected)

    def test_double(self):
        resp_input = ",1.23\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("1.23")
        self.assertEqual(actual, expected)

    def test_big_number(self):
        resp_input = "(3492890328409238509324850943850943825024385\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("3492890328409238509324850943850943825024385")
        self.assertEqual(actual, expected)

    def test_simple_error(self):
        resp_input = "-ERR unknown command\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("ERR unknown command")
        self.assertEqual(actual, expected)

    # ------------------------------
    # --------- Bulk Types ---------
    # ------------------------------

    def test_bulk_string_basic(self):
        resp_input = "$6\r\nfoobar\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("foobar")
        self.assertEqual(actual, expected)

    def test_bulk_string_empty(self):
        resp_input = "$0\r\n\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("")
        self.assertEqual(actual, expected)

    def test_bulk_string_null(self):
        resp_input = "$-1\r\n"
        actual = decoder(resp_input)
        expected = OutputStr(NULL)
        self.assertEqual(actual, expected)

    def test_resp3_null(self):
        resp_input = "_\r\n"
        actual = decoder(resp_input)
        expected = OutputStr(NULL)
        self.assertEqual(actual, expected)

    def test_bulk_error(self):
        resp_input = "!21\r\nSYNTAX invalid syntax\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("SYNTAX invalid syntax")
        self.assertEqual(actual, expected)

    def test_verbatim_string(self):
        """
        The decoder strips the first 4 bytes (encoding + ":" of the content.
        """
        # Length 15: "txt:Some content" -> 3 (txt) + 1 (:) + 11 (content) = 15
        resp_input = "=15\r\ntxt:Some content\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("Some content")
        self.assertEqual(actual, expected)

    # ------------------------------
    # --- Simple Aggregate Types ---
    # ------------------------------

    def test_array_flat(self):
        """No recursive structure test."""
        resp_input = "*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n"
        actual = decoder(resp_input)
        # Using Tuple
        expected = OutputSeq((
            OutputStr("foo"),
            OutputStr("bar")
        ))
        self.assertEqual(actual, expected)

    def test_map_flat(self):
        """No recursive structure test."""
        resp_input = "%1\r\n+first\r\n:1\r\n"
        actual = decoder(resp_input)
        # Using frozendict
        expected = OutputMap(frozendict({
            OutputStr("first"): OutputStr("1")
        }))
        self.assertEqual(actual, expected)

    def test_set_flat(self):
        resp_input = "~2\r\n+a\r\n+b\r\n"
        actual = decoder(resp_input)
        expected = OutputSeq((
            OutputStr("a"),
            OutputStr("b")
        ))
        self.assertEqual(actual, expected)

    def test_push(self):
        resp_input = ">3\r\n+pubsub\r\n+channel1\r\n+msg1\r\n"
        actual = decoder(resp_input)
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
        resp_input = (
            "*2\r\n"
            "+Level1\r\n"
            "*2\r\n"
            "+Level2\r\n"
            "*1\r\n"
            "+Level3\r\n"
        )
        actual = decoder(resp_input)
        
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
        resp_input = (
            "*2\r\n"
            "+Meta\r\n"
            "%1\r\n"
            "+Key\r\n"
            "+Value\r\n"
        )
        actual = decoder(resp_input)
        
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
        resp_input = (
            "%1\r\n"
            "+ListKey\r\n"
            "*2\r\n"
            ":1\r\n"
            ":2\r\n"
        )
        actual = decoder(resp_input)

        # Frozendict containing a Tuple
        expected = OutputMap(frozendict({
            OutputStr("ListKey"): OutputSeq((
                OutputStr("1"),
                OutputStr("2")
            ))
        }))
        self.assertEqual(actual, expected)

    # ------------------------------
    # --------- Exceptions ---------
    # ------------------------------
    # All decoder exceptions are wrapped in RuntimeError("Decoder failure.")

    def test_invalid_start_byte(self):
        resp_input = "?INVALID\r\n"

        with self.assertRaises(RuntimeError) as cm:
            decoder(resp_input)
        
        self.assertIsInstance(cm.exception.__cause__, KeyError)

    def test_invalid_crlf_termination(self):
        resp_input = "+NoEnd"
        with self.assertRaises(RuntimeError) as cm:
            decoder(resp_input)
        self.assertIsInstance(cm.exception.__cause__, ValueError)

    # ------------------------------
    # --- Complex Attribute Test ---
    # ------------------------------

    def test_complex_attributes(self):
        """
        Structure: |1 {source-command: 'GET'} *2 [ %2 {id: 1024, addr: ...}, %2 {id: 1025, addr: ...} ].
        """
        resp_input = (
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
        actual = decoder(resp_input)

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

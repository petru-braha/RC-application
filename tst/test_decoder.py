from unittest import TestCase
from src.protocol.constants_resp import *
from src.protocol.decoder import decoder
from src.protocol.output import OutputStr, OutputList, OutputDict

class TestDecoder(TestCase):

    # --- Scalar / Simple Types ---

    def test_simple_string(self):
        """Test simple strings (+)."""
        resp_input = "+OK\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("OK")
        self.assertEqual(actual, expected)

    def test_integer(self):
        """Test integers (:). Decoded as strings in this implementation."""
        resp_input = ":1000\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("1000")
        self.assertEqual(actual, expected)

    def test_boolean(self):
        """Test booleans (#)."""
        resp_input = "#t\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("t")
        self.assertEqual(actual, expected)

    def test_double(self):
        """Test doubles (,)."""
        resp_input = ",1.23\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("1.23")
        self.assertEqual(actual, expected)

    def test_big_number(self):
        """Test big numbers (()."""
        resp_input = "(3492890328409238509324850943850943825024385\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("3492890328409238509324850943850943825024385")
        self.assertEqual(actual, expected)

    def test_simple_error(self):
        """Test simple errors (-)."""
        resp_input = "-ERR unknown command\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("ERR unknown command")
        self.assertEqual(actual, expected)

    # --- Bulk Types ---

    def test_bulk_string_basic(self):
        """Test standard bulk string ($)."""
        resp_input = "$6\r\nfoobar\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("foobar")
        self.assertEqual(actual, expected)

    def test_bulk_string_empty(self):
        """Test empty bulk string."""
        resp_input = "$0\r\n\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("")
        self.assertEqual(actual, expected)

    def test_bulk_string_null(self):
        """Test null bulk string ($-1)."""
        resp_input = "$-1\r\n"
        actual = decoder(resp_input)
        expected = OutputStr(NULL)
        self.assertEqual(actual, expected)

    def test_resp3_null(self):
        """Test RESP3 null type (_)."""
        resp_input = "_\r\n"
        actual = decoder(resp_input)
        expected = OutputStr(NULL)
        self.assertEqual(actual, expected)

    def test_bulk_error(self):
        """Test bulk errors (!). Format: !<length>\r\n<error>\r\n."""
        resp_input = "!21\r\nSYNTAX invalid syntax\r\n"
        actual = decoder(resp_input)
        expected = OutputStr("SYNTAX invalid syntax")
        self.assertEqual(actual, expected)

    def test_verbatim_string(self):
        """
        Test verbatim strings (=).
        Format: =<length>\r\n<encoding>:<data>\r\n
        The decoder strips the first 4 bytes (encoding + :) of the content.
        """
        # Length 15: "txt:Some content" -> 3 (txt) + 1 (:) + 11 (content) = 15
        resp_input = "=15\r\ntxt:Some content\r\n"
        actual = decoder(resp_input)
        # Expected behavior: returns "Some content" (skips "txt:")
        expected = OutputStr("Some content")
        self.assertEqual(actual, expected)

    # --- Aggregate Types (Recursive) ---

    def test_array_flat(self):
        """Test flat array (*)."""
        resp_input = "*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n"
        actual = decoder(resp_input)
        expected = OutputList([
            OutputStr("foo"),
            OutputStr("bar")
        ])
        self.assertEqual(actual, expected)

    def test_map_flat(self):
        """Test map (%)."""
        resp_input = "%1\r\n+first\r\n:1\r\n"
        actual = decoder(resp_input)
        expected = OutputDict({
            OutputStr("first"): OutputStr("1")
        })
        self.assertEqual(actual, expected)

    def test_set_as_aggregate(self):
        """Test sets (~). Code treats them as aggregates (List)."""
        resp_input = "~2\r\n+a\r\n+b\r\n"
        actual = decoder(resp_input)
        expected = OutputList([
            OutputStr("a"),
            OutputStr("b")
        ])
        self.assertEqual(actual, expected)

    def test_recursive_nested_array(self):
        """
        Test nested arrays.
        Structure: [ "Level1", [ "Level2", [ "Level3" ] ] ]
        """
        resp_input = (
            "*2\r\n"
            "+Level1\r\n"
            "*2\r\n"          # Nested Array start
            "+Level2\r\n"
            "*1\r\n"      # Deeply nested Array start
            "+Level3\r\n"
        )
        actual = decoder(resp_input)
        
        expected = OutputList([
            OutputStr("Level1"),
            OutputList([
                OutputStr("Level2"),
                OutputList([
                    OutputStr("Level3")
                ])
            ])
        ])
        self.assertEqual(actual, expected)

    def test_recursive_map_in_array(self):
        """
        Test a Map nested inside an Array.
        Structure: [ "Meta", { "Key": "Value" } ]
        """
        resp_input = (
            "*2\r\n"
            "+Meta\r\n"
            "%1\r\n"          # Map start
            "+Key\r\n"
            "+Value\r\n"
        )
        actual = decoder(resp_input)
        
        expected = OutputList([
            OutputStr("Meta"),
            OutputDict({
                OutputStr("Key"): OutputStr("Value")
            })
        ])
        self.assertEqual(actual, expected)

    def test_recursive_array_in_map(self):
        """
        Test an Array nested inside a Map value.
        Structure: { "ListKey": [1, 2] }
        """
        resp_input = (
            "%1\r\n"
            "+ListKey\r\n"
            "*2\r\n"
            ":1\r\n"
            ":2\r\n"
        )
        actual = decoder(resp_input)

        expected = OutputDict({
            OutputStr("ListKey"): OutputList([
                OutputStr("1"),
                OutputStr("2")
            ])
        })
        self.assertEqual(actual, expected)

    # --- Edge Cases & Errors ---

    def test_invalid_start_byte(self):
        """Test that unknown symbols raise KeyError."""
        resp_input = "?INVALID\r\n"
        # The code wraps exceptions in RuntimeError("Decoder failure.")
        with self.assertRaises(RuntimeError) as cm:
            decoder(resp_input)
        
        # Verify the cause was likely the KeyError from the dictionary lookup
        self.assertIsInstance(cm.exception.__cause__, KeyError)

    def test_invalid_crlf_termination(self):
        """Test malformed string without CRLF."""
        resp_input = "+NoEnd"
        with self.assertRaises(RuntimeError) as cm:
            decoder(resp_input)
        # Should be ValueError inside
        self.assertIsInstance(cm.exception.__cause__, ValueError)

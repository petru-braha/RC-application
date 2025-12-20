from unittest import TestCase
from frozendict import frozendict

from src.protocol.formatter import formatter
from src.protocol.output import Output, OutputStr, OutputSeq, OutputMap, OutputAtt

class TestFormatter(TestCase):

    # ------------------------------
    # --------- Strings ------------
    # ------------------------------

    def test_output_str(self):
        input_obj = OutputStr("OK")
        actual = formatter(input_obj)
        expected = "OK\r\n"
        self.assertEqual(actual, expected)

    def test_output_str_with_prefix(self):
        """Test string formatting with a manual prefix (internal logic check)."""
        input_obj = OutputStr("val")
        # Manually verify internal helper behavior via main entry point logic.
        # This simulates what happens inside a nested structure.
        actual = formatter(input_obj, prefix="   ")
        expected = "   val\r\n"
        self.assertEqual(actual, expected)

    # ------------------------------
    # --------- Sequences ----------
    # ------------------------------

    def test_output_seq_flat(self):
        """No recursive structure test."""
        input_obj = OutputSeq((
            OutputStr("one"),
            OutputStr("two"),
            OutputStr("three")
        ))
        actual = formatter(input_obj)
        expected = (
            "1) one\r\n"
            "2) two\r\n"
            "3) three\r\n"
        )
        self.assertEqual(actual, expected)

    def test_output_seq_empty(self):
        input_obj = OutputSeq(())
        actual = formatter(input_obj)
        expected = "(empty sequence)\r\n"
        self.assertEqual(actual, expected)

    def test_output_seq_nested(self):
        """
        Structure: [ "Level1", [ "Level2" ] ].
        """
        input_obj = OutputSeq((
            OutputStr("Level1"),
            OutputSeq((
                OutputStr("Level2"),
            ))
        ))
        actual = formatter(input_obj)
        expected = (
            "1) Level1\r\n"
            "2) 1) Level2\r\n"
        )
        self.assertEqual(actual, expected)

    # ------------------------------
    # ------------ Maps ------------
    # ------------------------------

    def test_output_map_flat(self):
        """No recursive structure test."""
        input_obj = OutputMap(frozendict({
            OutputStr("key1"): OutputStr("value1"),
            OutputStr("key2"): OutputStr("value2")
        }))
        actual = formatter(input_obj)
        
        # Note: dict iteration order is insertion-ordered in modern Python.
        # For robustness, we assume standard insertion order here.
        expected = (
            "1) key1\r\n"
            "2) value1\r\n"
            "3) key2\r\n"
            "4) value2\r\n"
        )
        self.assertEqual(actual, expected)

    def test_output_map_empty(self):
        input_obj = OutputMap(frozendict({}))
        actual = formatter(input_obj)
        expected = "(empty map)\r\n"
        self.assertEqual(actual, expected)

    def test_output_map_nested_seq(self):
        """
        Structure: { "list": ["A", "B"] }.
        """
        input_obj = OutputMap(frozendict({
            OutputStr("list"): OutputSeq((
                OutputStr("A"),
                OutputStr("B")
            ))
        }))
        actual = formatter(input_obj)
        expected = (
            "1) list\r\n"
            "2) 1) A\r\n"
            "   2) B\r\n"
        )
        self.assertEqual(actual, expected)

    # ------------------------------
    # --------- Attributes ---------
    # ------------------------------

    def test_output_att(self):
        """
        Structure: Attributes { "meta": "data" }, Payload: "RealData".
        """
        input_obj = OutputAtt(
            attributes=OutputMap(frozendict({
                OutputStr("meta"): OutputStr("data")
            })),
            payload=OutputStr("RealData")
        )
        actual = formatter(input_obj)
        expected = (
            "Attributes:\r\n"
            "1) meta\r\n"
            "2) data\r\n"
            "Payload:\r\n"
            "RealData\r\n"
        )
        self.assertEqual(actual, expected)

    def test_output_att_in_seq(self):
        """
        Test Attribute inside a Sequence (verifying prefix handling).
        Structure: [ "Item1", Attributed("Item2") ].
        """
        input_obj = OutputSeq((
            OutputStr("Item1"),
            OutputAtt(
                attributes=OutputMap(frozendict({
                    OutputStr("ttl"): OutputStr("100")
                })),
                payload=OutputStr("Item2")
            )
        ))
        actual = formatter(input_obj)
        
        expected = (
            "1) Item1\r\n"
            "   Attributes:\r\n"
            "   1) ttl\r\n"
            "   2) 100\r\n"
            "   Payload:\r\n"
            "2) Item2\r\n"
        )
        self.assertEqual(actual, expected)

    def test_output_att_empty(self):
        input_obj = OutputAtt(
            attributes=OutputMap(frozendict({})),
            payload=OutputStr("Data")
        )
        actual = formatter(input_obj)
        expected = (
            "Data\r\n"
        )
        self.assertEqual(actual, expected)

    # ------------------------------
    # --- Complex/Edge Cases -------
    # ------------------------------

    def test_complex_nested_structure(self):
        """
        Test a highly recursive structure with mixed types.
        """
        input_obj = OutputMap(frozendict({
            OutputStr("key1"): OutputStr("val1"),
            OutputStr("key2"): OutputSeq((
                OutputStr("sub1"),
                OutputStr("sub2"),
                OutputSeq((
                    OutputMap(frozendict({
                        OutputStr("key4"): OutputMap(frozendict({
                            OutputStr("deepKey"): OutputStr("deepVal")
                        }))
                    })),
                    OutputSeq(()),
                    OutputMap(frozendict({}))
                ))
            ))
        }))

        actual = formatter(input_obj)
        
        expected = (
            "1) key1\r\n"
            "2) val1\r\n"
            "3) key2\r\n"
            "4) 1) sub1\r\n"
            "   2) sub2\r\n"
            "   3) 1) 1) key4\r\n"
            "         2) 1) deepKey\r\n"
            "            2) deepVal\r\n"
            "      2) (empty sequence)\r\n"
            "      3) (empty map)\r\n"
        )
        self.assertEqual(expected, actual, f"cacat {actual}")

    def test_unknown_output_type(self):
        """Test assertion error for unknown output types."""
        class UnknownOutput(Output):
            pass
            
        with self.assertRaises(AssertionError):
            formatter(UnknownOutput())

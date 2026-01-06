from frozendict import frozendict
from unittest import TestCase

from src.protocol.output import OutputStr, OutputSeq, OutputMap

class TestOutput(TestCase):
    
    def test_seq_simple(self):
        output = OutputSeq((
            OutputStr("a"), 
            OutputStr("b")
        ))
        
        expected = (
            "1) a\n"
            "2) b\n"
        )
        self.assertEqual(str(output), expected)

    def test_map_simple(self):
        output = OutputMap(frozendict({
            OutputStr("k"): OutputStr("v")
        }))
        
        expected = (
            "1) k\n"
            "2) v\n"
        )
        self.assertEqual(str(output), expected)

    def test_complex_recursive(self):
        """
        Verify formatting of a complex nested structure: Map -> Sequence -> Maps.
        
        Structure Mock:
        {
            "users": [
                { "id": "1" },
                { "id": "2" }
            ]
        }
        """
        output = OutputMap(frozendict({
            OutputStr("users"): OutputSeq((
                OutputMap(frozendict({OutputStr("id"): OutputStr("1")})),
                OutputMap(frozendict({OutputStr("id"): OutputStr("2")}))
            ))
        }))
        
        expected = (
            "1) users\n"
            "2) 1) 1) id\n"
            "      2) 1\n"
            "   2) 1) id\n"
            "      2) 2\n"
        )
        self.assertEqual(str(output), expected)

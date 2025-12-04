from src import parser
from unittest import TestCase

class TestParser(TestCase):
    def test_valid_input(self):
        inputs = [
            "set dada 1",
            "set    dada  1 "
        ]
        for input in inputs:
            cmd, argv = parser(input)
            self.assertEqual(cmd, "set")
            self.assertEqual(argv, ["dada", "1"])
        
    def test_empty_input(self):
        inputs = [
            "",
            "12",
            "se"
        ]
        for input in inputs:
            self.assertRaises(ValueError, lambda: parser(input))

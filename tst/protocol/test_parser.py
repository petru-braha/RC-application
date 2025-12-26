from unittest import TestCase
from src.protocol.parser import parser
from src.protocol.exceptions import QuoteError, SpaceError, ParserError

class TestParser(TestCase):
    """
    We test the parser only.
    Input validation is done within the sanitizer module.
    """
    
    def test_valid_input(self):
        """
        Also tests the ignoring of the extra spaces.
        """
        inputs = [
            "set dada 1",
            "   set    dada  1 ",
            "set dada 1   "
        ]
        for input in inputs:
            cmd, argv = parser(input)
            self.assertEqual(cmd, "set")
            self.assertEqual(argv, ["dada", "1"])
        
    def test_empty_input(self):
        inputs = [
            "",
            " ",
            "12",
            "se"
        ]
        for input in inputs:
            self.assertRaises(ValueError, lambda: parser(input))

    def test_single_token(self):
        cmd, argv = parser("incr")
        self.assertEqual(cmd, "incr")
        self.assertEqual(argv, [])

    def test_arguments_must_be_space_separated(self):
        inputs = [
            "set \"dada\"1",     # User typed: SET "dada"1
            "set \"dada\"\"1\"", # User typed: SET "dada""1"
            "set \"dada\"\'1\'", # User typed: SET "dada"'1'
            "set \'dada\'1",     # User typed: SET 'dada'1
            "set \'dada\'\'1\'", # User typed: SET 'dada''1'
            "set \'dada\' \"1\" \"2\"\"3\"", # User typed: SET 'dada' "1" "2""3"
        ]
        for input in inputs:
            self.assertRaises(SpaceError, lambda: parser(input))
        
    def test_valid_quotes(self):
        """
        Tests if both \" and \' behave likewise.
        """
        inputs = [
            "set dada \"new text\"",
            "set dada \'new text\'",
        ]
        for input in inputs:
            cmd, argv = parser(input)
            self.assertEqual(cmd, "set")
            self.assertEqual(argv, ["dada", "new text"])
    
    def test_unclosed_quotes(self):
        inputs = [
            "HSET dada \"abc 1 west 2",
            "HSET dada \"abc\" 1 west \"2",
            "HSET dada \"xyz 2 \"east duck\" \"3",
            # This is a special case that should result in the same bahaviour.
            "set dada \"new text\\",
        ]
        for input in inputs:
            self.assertRaises(ParserError, lambda: parser(input))
    
    def test_unquoted_must_not_contain_quotes(self):
        inputs = [
            "set dada 1\"3",
            "set da\"d\"a 1",
        ]
        for input in inputs:
            self.assertRaises(QuoteError, lambda: parser(input))

    def test_escape_handling_inside_quotes(self):
        inputs = [
            "set dada \"1\\n2\" ",
            "set dada \" \\\" \" ",
            "set dada \" \\\' \" ",
            "set dada \" \' \" ",
            # Here test all the accepted escaped sequences for both quote types.
            "set dada \" \\n \\r \\t \\b \\a \\\\ \" ",
            "set dada \' \\\' \\\\ \' ",
            # Unsupported escapes, no transformation expected.
            "set dada \' \\n \\r \\t \\b \\a \' ",
            # Backslash not backed by an escapable character.
            "set dada \" \\ \\ a \" "
        ]

        _, argv = parser(inputs[0]); self.assertEqual(argv[1], "1\n2")
        _, argv = parser(inputs[1]); self.assertEqual(argv[1], " \" ")
        _, argv = parser(inputs[2]); self.assertEqual(argv[1], " \\\' ")
        _, argv = parser(inputs[3]); self.assertEqual(argv[1], " \' ")
        _, argv = parser(inputs[4]); self.assertEqual(argv[1], " \n \r \t \b \a \\ ")
        _, argv = parser(inputs[5]); self.assertEqual(argv[1], " \' \\ ")
        _, argv = parser(inputs[6]); self.assertEqual(argv[1], " \\n \\r \\t \\b \\a ")
        _, argv = parser(inputs[7]); self.assertEqual(argv[1], " \\ \\ a ")

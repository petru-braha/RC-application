import unittest
import logging
from unittest.mock import patch, MagicMock
from core.config import Config, Stage

class TestConfig(unittest.TestCase):
    def setUp(self):
        # Reset Config state before each test
        Config.cli = False
        Config.stage = Stage.DEV
        Config.tls_enforced = False
        Config.max_connections = Config.DEFAULT_MAX_CONNECTIONS

    def test_init_defaults(self):
        """Test initialization with empty dotenv dict."""
        with patch('sys.argv', ['main.py']):
            Config.init({})
            
        self.assertFalse(Config.cli)
        self.assertEqual(Config.stage, Stage.DEV)
        self.assertFalse(Config.tls_enforced)
        self.assertEqual(Config.max_connections, Config.DEFAULT_MAX_CONNECTIONS)
        
        # Verify handlers exist
        self.assertIsInstance(Config.file_handler, logging.FileHandler)
        self.assertIsInstance(Config.stdout_handler, logging.StreamHandler)
        self.assertIsInstance(Config.stderr_handler, logging.StreamHandler)

    def test_init_overrides(self):
        """Test initialization with dotenv values."""
        dotenv = {
            "stage": "PROD",
            "tls_enforced": "True",
            "max_connections": "2048",
            "debug": "custom_debug.log"
        }
        
        with patch('sys.argv', ['main.py', '--cli']):
            Config.init(dotenv)

        self.assertTrue(Config.cli)
        self.assertEqual(Config.stage, Stage.PROD)
        
        # This highlights the potential boolean conversion issue
        # If "False" string is passed, bool("False") is True
        self.assertTrue(Config.tls_enforced) 
        
        self.assertEqual(Config.max_connections, 2048)
        self.assertTrue(isinstance(Config.file_handler, logging.FileHandler))
        # Check if the filename matches (cleaning up path differences)
        from os.path import basename
        self.assertEqual(basename(Config.file_handler.baseFilename), "custom_debug.log")

    def test_bool_conversion_issue(self):
        """Demonstrate the bool conversion issue."""
        dotenv = {"tls_enforced": "False"} # String "False"
        Config.init(dotenv)
        # Expecting False, but current implementation might make it True
        self.assertTrue(Config.tls_enforced, "bool('False') evaluates to True in current impl")

if __name__ == '__main__':
    unittest.main()

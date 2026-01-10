import importlib
import logging
from unittest import TestCase
from unittest.mock import patch, MagicMock
import sys

from src.core import config
from src.core.constants import StageEnum

class TestConfig(TestCase):
    
    dotenv_patcher = patch("dotenv.dotenv_values")
    file_patcher = patch("logging.FileHandler")
    stream_patcher = patch("logging.StreamHandler")
    
    def setUp(self):
        self.mock_dotenv = TestConfig.dotenv_patcher.start()
        self.mock_file = TestConfig.file_patcher.start()
        self.mock_stream = TestConfig.stream_patcher.start()
        
        self.mock_stream.side_effect = lambda *args, **kwargs: MagicMock()

    def tearDown(self):
        TestConfig.dotenv_patcher.stop()
        TestConfig.file_patcher.stop()
        TestConfig.stream_patcher.stop()

    def test_defaults(self):
        """
        Test configuration with empty .env file (should use defaults).
        """
        self.mock_dotenv.return_value = {}
        importlib.reload(config)
        
        self.assertEqual(config.STAGE, StageEnum.DEV)
        self.assertFalse(config.TLS_ENFORCED)
        self.assertEqual(config.MAX_CONNECTIONS, 1024)
        
        # Verify default log file was created (among other calls)
        self.mock_file.assert_any_call("./log/debug.log")
        self.mock_stream.assert_any_call(sys.stdout)
        self.mock_stream.assert_any_call(sys.stderr)

    def test_custom_values(self):
        """
        Test configuration with valid values in .env.
        """
        self.mock_dotenv.return_value = {
            "STAGE": "PROD",
            "TLS_ENFORCED": "TRUE",
            "MAX_CONNECTIONS": "100",
            "FILE_HANDLER": "custom.log",
            "STDOUT_HANDLER": "out/custom.log",
            "STDERR_HANDLER": "err/custom.log"
        }
        importlib.reload(config)
        
        self.assertEqual(config.STAGE, StageEnum.PROD)
        self.assertTrue(config.TLS_ENFORCED)
        self.assertEqual(config.MAX_CONNECTIONS, 100)
        
        self.mock_file.assert_any_call("custom.log")
        self.mock_file.assert_any_call("out/custom.log")
        self.mock_file.assert_any_call("err/custom.log")
    
    def test_valid_stage(self):
        inputs = [
            "DEV", "PROD",
            "dev", "prod",
            "Dev", "Prod",
            "dEv", "pRoD"
        ]
        for input in inputs:
            self.mock_dotenv.return_value = {"STAGE": input}
            importlib.reload(config)
            
            self.assertEqual(config.STAGE, StageEnum[input.upper()])
            self.assertFalse(config._found_invalid)
    
    def test_invalid_stage(self):
        self.mock_dotenv.return_value = {"STAGE": "ALPHA_4"}
        importlib.reload(config)
        
        self.assertEqual(config.STAGE, StageEnum.DEV)
        self.assertTrue(config._found_invalid)
    
    def test_valid_tls_enforced(self):
        inputs = [
            "TRUE", "FALSE",
            "true", "false",
            "True", "False",
            "tRuE", "fAlSe"          
        ]
        prev_input = False
        for input in inputs:
            self.mock_dotenv.return_value = {"TLS_ENFORCED": input}
            importlib.reload(config)
            
            prev_input = not prev_input
            self.assertEqual(config.TLS_ENFORCED, prev_input)
            self.assertFalse(config._found_invalid)
    
    def test_invalid_tls_enforced(self):
        self.mock_dotenv.return_value = {"TLS_ENFORCED": "NOT_A_BOOL"}
        importlib.reload(config)
        
        self.assertEqual(config.STAGE, StageEnum.DEV)
        self.assertTrue(config._found_invalid)
    
    def test_valid_max_connections(self):
        inputs = ["0", "1", "256", "1023"]
        for input in inputs:
            self.mock_dotenv.return_value = {"MAX_CONNECTIONS": input}
            importlib.reload(config)
            
            self.assertEqual(config.MAX_CONNECTIONS, int(input))
            self.assertFalse(config._found_invalid)
    
    def test_invalid_max_connections(self):
        # Case 1: Non-integer.
        self.mock_dotenv.return_value = {"MAX_CONNECTIONS": "not_an_int"}
        importlib.reload(config)
        self.assertEqual(config.MAX_CONNECTIONS, 1024)
        self.assertTrue(config._found_invalid)

        # Case 2: Out of bounds (negative).
        self.mock_dotenv.return_value = {"MAX_CONNECTIONS": "-1"}
        importlib.reload(config)
        self.assertEqual(config.MAX_CONNECTIONS, 1024)
        self.assertTrue(config._found_invalid)

        # Case 3: Out of bounds (too large).
        self.mock_dotenv.return_value = {"MAX_CONNECTIONS": "1025"}
        importlib.reload(config)
        self.assertEqual(config.MAX_CONNECTIONS, 1024)
        self.assertTrue(config._found_invalid)

    def test_handlers_configuration(self):
        self.mock_dotenv.return_value = {}
        importlib.reload(config)
        
        file_handler = config.FILE_HANDLER
        file_handler.setLevel.assert_called_with(logging.DEBUG)
        file_handler.setFormatter.assert_called()
        file_handler.addFilter.assert_called()
        
        stdout_handler = config.STDOUT_HANDLER
        stdout_handler.setLevel.assert_called_with(logging.DEBUG)
        stdout_handler.setFormatter.assert_called()
        stdout_handler.addFilter.assert_called()
        
        stderr_handler = config.STDERR_HANDLER
        stderr_handler.setLevel.assert_called_with(logging.WARNING)
        stderr_handler.setFormatter.assert_called()

    def test_invalid_handler_paths(self):
        bad_path = "/etc/passwds/bad.log"
        good_path = "/var/log/users.log"
        cool_path = "./path/that/does/not/exist/cool.log"
        
        def side_effect(filename, *args, **kwargs):
            # This logic is dependent on the file system of the user.
            # It is okay to model the behavior as so, FileNotFoundError is desired to be raised. 
            if filename in [bad_path, good_path, cool_path]:
                raise FileNotFoundError
            return MagicMock()
            
        self.mock_file.side_effect = side_effect
        self.mock_dotenv.return_value = {
            "FILE_HANDLER": bad_path,
            "STDOUT_HANDLER": good_path,
            "STDERR_HANDLER": cool_path
        }
        importlib.reload(config)

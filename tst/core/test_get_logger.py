from unittest import TestCase
from unittest.mock import patch, MagicMock
import logging

from src.core.get_logger import get_logger
from src.core.constants import StageEnum

class TestGetLogger(TestCase):
    
    @patch("src.core.get_logger.logging")
    @patch("src.core.get_logger.STDERR_HANDLER")
    @patch("src.core.get_logger.STDOUT_HANDLER")
    @patch("src.core.get_logger.FILE_HANDLER")
    @patch("src.core.get_logger.STAGE", StageEnum.DEV)
    def test_get_logger_dev(self, mock_file, mock_stdout, mock_stderr, mock_logging):
        logger_mock = MagicMock()
        mock_logging.getLogger.return_value = logger_mock
        mock_logging.DEBUG = logging.DEBUG
        
        logger = get_logger("test_logger")
        
        mock_logging.getLogger.assert_called_with("test_logger")
        logger_mock.setLevel.assert_called_with(logging.DEBUG)
        
        logger_mock.addHandler.assert_any_call(mock_file)
        logger_mock.addHandler.assert_any_call(mock_stdout)
        logger_mock.addHandler.assert_any_call(mock_stderr)
        
        self.assertEqual(logger, logger_mock)

    @patch("src.core.get_logger.logging")
    @patch("src.core.get_logger.STDERR_HANDLER")
    @patch("src.core.get_logger.STDOUT_HANDLER")
    @patch("src.core.get_logger.FILE_HANDLER")
    @patch("src.core.get_logger.STAGE", StageEnum.PROD)
    def test_get_logger_prod(self, mock_file, mock_stdout, mock_stderr, mock_logging):
        logger_mock = MagicMock()
        mock_logging.getLogger.return_value = logger_mock
        mock_logging.INFO = logging.INFO
        
        logger = get_logger("test_logger")
        
        mock_logging.getLogger.assert_called_with("test_logger")
        logger_mock.setLevel.assert_called_with(logging.INFO)
        
        logger_mock.addHandler.assert_any_call(mock_file)
        logger_mock.addHandler.assert_any_call(mock_stdout)
        logger_mock.addHandler.assert_any_call(mock_stderr)
        
        self.assertEqual(logger, logger_mock)

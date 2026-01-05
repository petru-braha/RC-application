"""
Centralized configuration manager for the application and logging.

Handles initialization of global settings, logging, and environment variables.
Determines execution mode (CLI vs GUI) and manages connection parameters.
"""
from dotenv import dotenv_values
from enum import IntEnum
import logging
import os
import sys

from .util import LogCompressor

# Keep this as an enum since it can be extended to much more (e.g. testing).
class Stage(IntEnum):
    PROD = 0
    DEV = 1

# Fixed utilities used to initialize the current application session constants.
_MIN_CONNECTIONS: int = 0
"""
Minimum allowed concurrent client connections.
"""
_DEFAULT_MAX_CONNECTIONS: int = 1024
"""
Maximum allowed concurrent client connections.
"""
_DEFAULT_LOG_FILE: str = "./log/debug.log"
"""
Default path for the log file.
"""

# See more: https://docs.python.org/3/library/logging.html#logrecord-attributes
_VERBOSE_FORMAT: str = "%(asctime)s %(levelname)s <%(name)s[%(lineno)d]> --- %(message)s"
"""
Format string for verbose logging (used in file logs).
"""
_DANGER_FORMAT: str = "%(levelname)s <%(name)s[%(lineno)d]> --- %(message)s"
"""
Format string for warnings and errors logging.
"""
_SIMPLE_FORMAT: str = "%(levelname)s <%(name)s> --- %(message)s"
"""
Format string for simple logging (used in console output).
"""

def _parse_dotenv():
    global STAGE, TLS_ENFORCED, MAX_CONNECTIONS, FILE_HANDLER, STDOUT_HANDLER, STDERR_HANDLER
    dotenv_dict = dotenv_values()
    
    app_configs = [
        ("STAGE", lambda x: Stage[x.upper()]),
        ("TLS_ENFORCED", lambda x: str(x).lower() == "true"),
        ("MAX_CONNECTIONS", int),
        ("FILE_HANDLER", logging.FileHandler),
        ("STDOUT_HANDLER", logging.FileHandler),
        ("STDERR_HANDLER", logging.FileHandler)
    ]
    for key, func in app_configs:
        try:
            val = dotenv_dict[key]
            globals()[key] = func(val)
        except (KeyError, ValueError, OSError):
            pass

    # Ensure log directory exists if we use the default log file.
    os.makedirs(os.path.dirname(_DEFAULT_LOG_FILE), exist_ok=True)

    if MAX_CONNECTIONS < _MIN_CONNECTIONS or MAX_CONNECTIONS > _DEFAULT_MAX_CONNECTIONS:
        MAX_CONNECTIONS = _DEFAULT_MAX_CONNECTIONS
    
    # Initialize handlers if they weren't specified but dotenv.
    if FILE_HANDLER == None:
        FILE_HANDLER = logging.FileHandler(_DEFAULT_LOG_FILE)
    if STDOUT_HANDLER == None:
        STDOUT_HANDLER = logging.StreamHandler(sys.stdout)
    if STDERR_HANDLER == None:
        STDERR_HANDLER = logging.StreamHandler(sys.stderr)

# The importable values can be found below
IS_CLI: bool = len(sys.argv) > 1 and sys.argv[1] == "--cli"
"""
Indicates if the application is running in Command Line Interface mode.
"""
STAGE: Stage = Stage.DEV
"""
Current deployment stage (PROD, DEV, etc.).
"""
TLS_ENFORCED: bool = False
"""
Whether TLS encryption is enforced for connections.
"""
MAX_CONNECTIONS: int = _DEFAULT_MAX_CONNECTIONS
"""
Maximum allowed concurrent connections.
"""

# Do not initialize handlers directly since consumes extra resources and it is bug prone.
FILE_HANDLER: logging.Handler | None = None
"""
Logging handler for writing debug logs to a file.
"""
STDOUT_HANDLER: logging.Handler | None = None
"""
Logging handler for writing info loops to standard output.
"""
STDERR_HANDLER: logging.Handler | None = None
"""
Logging handler for writing warnings and errors to standard error.
"""

_parse_dotenv()

FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(logging.Formatter(_VERBOSE_FORMAT))
FILE_HANDLER.addFilter(lambda r: r.levelno == logging.DEBUG)

STDOUT_HANDLER.setLevel(logging.DEBUG)
STDOUT_HANDLER.setFormatter(
    LogCompressor(_SIMPLE_FORMAT, LogCompressor.DEFAULT_MAX_BYTES / 4))
STDOUT_HANDLER.addFilter(lambda r: r.levelno <= logging.INFO)
    
STDERR_HANDLER.setLevel(logging.WARNING)
STDERR_HANDLER.setFormatter(LogCompressor(_DANGER_FORMAT))

# The method that should be used by client modules.
def get_logger(name: str) -> logging.Logger:
    """
    Retrieves a configured logger instance.

    Attaches the standard file, stdout, and stderr handlers to the logger.

    Args:
        name (str): The name of the logger (usually __name__).

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    logger.addHandler(FILE_HANDLER)
    logger.addHandler(STDOUT_HANDLER)
    logger.addHandler(STDERR_HANDLER)

    return logger

# Finally log every assigned setting.
logger = get_logger(__name__)
logger.info("Configuration initialized.")
logger.info("Stage: %s", STAGE.name)
logger.info("TLS enforced: %s", TLS_ENFORCED)
logger.info("Max connections: %s", MAX_CONNECTIONS)
logger.info("File handler: %s", FILE_HANDLER)
logger.info("Stdout handler: %s", STDOUT_HANDLER)
logger.info("Stderr handler: %s", STDERR_HANDLER)
logger.info("Discrepancies between the active configuration and the \".env\" file indicate "
    "that the provided values were invalid and have reverted to their defaults.\n")

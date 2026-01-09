"""
Centralized configuration manager for the application and logging.

Handles initialization of global settings, logging, and environment variables.
Determines execution mode (CLI vs GUI) and manages connection parameters.
"""
from dotenv import dotenv_values
import logging
import os
import sys

from .constants import StageEnum
from .util import LogCompressor

__all__ = ["IS_CLI", "STAGE", "TLS_ENFORCED", "MAX_CONNECTIONS",
           "FILE_HANDLER", "STDOUT_HANDLER", "STDERR_HANDLER"]

_dotenv_dict = dotenv_values()
_found_invalid = False

# ------------------------------------------------------------
# -------------------------- IS_CLI --------------------------
# ------------------------------------------------------------

IS_CLI = len(sys.argv) > 1 and sys.argv[1] == "--cli"
"""
Indicates if the application is running in Command Line Interface mode.
"""

# ------------------------------------------------------------
# -------------------------- STAGE ---------------------------
# ------------------------------------------------------------

_stage = StageEnum.DEV
try:
    _stage_str = _dotenv_dict.get("STAGE")
    if _stage_str is not None:
        _stage = StageEnum[_stage_str.upper()]
except KeyError:
    _found_invalid = True

STAGE: StageEnum = _stage
"""
Current deployment stage (PROD, DEV, etc.).
"""

# ------------------------------------------------------------
# ----------------------- TLS_ENFORCED -----------------------
# ------------------------------------------------------------

_tls_enforced_bool = False
try:
    _tls_enforced_str = _dotenv_dict.get("TLS_ENFORCED")
    if _tls_enforced_str is not None:
        _tls_enforced_str = _tls_enforced_str.upper()
        if _tls_enforced_str == "TRUE":
            _tls_enforced_bool = True
        elif _tls_enforced_str == "FALSE":
            _tls_enforced_bool = False
        else:
            raise ValueError
except ValueError:
    _found_invalid = True

TLS_ENFORCED = _tls_enforced_bool
"""
Whether TLS encryption is enforced for connections.
"""

# ------------------------------------------------------------
# --------------------- MAX_CONNECTIONS ----------------------
# ------------------------------------------------------------

# Fixed utilities used to initialize the current application session constants.
_MIN_CONNECTIONS = 0
"""
Minimum allowed concurrent client connections.
"""
_DEFAULT_MAX_CONNECTIONS = 1024
"""
Maximum allowed concurrent client connections.
"""

_max_connections = _DEFAULT_MAX_CONNECTIONS
try:
    _max_connections_str = _dotenv_dict.get("MAX_CONNECTIONS")
    if _max_connections_str is not None:
        _max_connections = int(_max_connections_str)
        if not _MIN_CONNECTIONS <= _max_connections < _DEFAULT_MAX_CONNECTIONS:
            _max_connections = _DEFAULT_MAX_CONNECTIONS
            raise ValueError
except ValueError:
    _found_invalid = True

MAX_CONNECTIONS = _max_connections
"""
Maximum allowed concurrent connections.
"""

# ------------------------------------------------------------
# ---------------------- LOG FORMATTERS ----------------------
# ------------------------------------------------------------

# See more: https://docs.python.org/3/library/logging.html#logrecord-attributes
_VERBOSE_FORMAT = "%(asctime)s %(levelname)s <%(name)s[%(lineno)d]> --- %(message)s"
"""
Format string for verbose logging (used in file logs).
"""
_DANGER_FORMAT = "%(levelname)s <%(name)s[%(lineno)d]> --- %(message)s"
"""
Format string for warnings and errors logging.
"""
_SIMPLE_FORMAT = "%(levelname)s <%(name)s> --- %(message)s"
"""
Format string for simple logging (used in console output).
"""
_DEFAULT_LOG_FILE = "./log/debug.log"
"""
Default path for the log file.
"""

# ------------------------------------------------------------
# ----------------------- FILE HANDLER -----------------------
# ------------------------------------------------------------

_file_handler = _dotenv_dict.get("FILE_HANDLER")
if _file_handler:
    _file_handler = logging.FileHandler(_file_handler)
else:
    # Ensure log directory exists if we use the default log file.
    os.makedirs(os.path.dirname(_DEFAULT_LOG_FILE), exist_ok=True)
    _file_handler = logging.FileHandler(_DEFAULT_LOG_FILE)

FILE_HANDLER = _file_handler
"""
Logging handler for writing debug logs to a file.
"""

FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(logging.Formatter(_VERBOSE_FORMAT))
FILE_HANDLER.addFilter(lambda r: r.levelno == logging.DEBUG)

# ------------------------------------------------------------
# ---------------------- STDOUT HANDLER ----------------------
# ------------------------------------------------------------

_stdout_handler = _dotenv_dict.get("STDOUT_HANDLER")
if _stdout_handler:
    _stdout_handler = logging.FileHandler(_stdout_handler)
else:
    _stdout_handler = logging.StreamHandler(sys.stdout)

STDOUT_HANDLER = _stdout_handler
"""
Logging handler for writing info loops to standard output.
"""

STDOUT_HANDLER.setLevel(logging.DEBUG)
STDOUT_HANDLER.setFormatter(
    LogCompressor(_SIMPLE_FORMAT, LogCompressor.DEFAULT_MAX_BYTES / 4))
STDOUT_HANDLER.addFilter(lambda r: r.levelno <= logging.INFO)

# ------------------------------------------------------------
# ---------------------- STDERR HANDLER ----------------------
# ------------------------------------------------------------

_stderr_handler = _dotenv_dict.get("STDERR_HANDLER")
if _stderr_handler:
    _stderr_handler = logging.FileHandler(_stderr_handler)
else:
    _stderr_handler = logging.StreamHandler(sys.stderr)

STDERR_HANDLER = _stderr_handler
"""
Logging handler for writing warnings and errors to standard error.
"""

STDERR_HANDLER.setLevel(logging.WARNING)
STDERR_HANDLER.setFormatter(LogCompressor(_DANGER_FORMAT))

# Finally log every assigned setting.
from .get_logger import get_logger
logger = get_logger(__name__)
logger.debug("Configuration initialized.")
logger.debug("Stage: %s", STAGE.name)
logger.debug("TLS enforced: %s", TLS_ENFORCED)
logger.debug("Max connections: %s", MAX_CONNECTIONS)
logger.debug("File handler: %s", FILE_HANDLER)
logger.debug("Stdout handler: %s", STDOUT_HANDLER)
logger.debug("Stderr handler: %s", STDERR_HANDLER)
if _found_invalid:
    logger.debug(
        "Discrepancies between the active configuration and the \".env\" file indicate "
        "that the provided values were invalid and have reverted to their defaults.\n")

"""
Core package providing the foundational infrastructure for the application.

This package serves as the base for the entire codebase and maintains zero
dependencies on other internal modules. It provides essential utilities,
constants, common interfaces, and application initialization logic.
"""

from .config import *
from .constants import *
from .exceptions import *
from .get_logger import get_logger
from .structs import Addr
from .util import Immutable, uninterruptible, process_redis_url

__all__ = ["Addr", "StageEnum", "Immutable",
           "RCError", "AssignmentError", "NetworkError",
           "PartialResponseError", "PartialRequestError", "ConnectionCountError",
           "IS_CLI", "STAGE", "TLS_ENFORCED", "MAX_CONNECTIONS",
           "FILE_HANDLER", "STDOUT_HANDLER", "STDERR_HANDLER",
           "get_logger", "uninterruptible", "process_redis_url"]

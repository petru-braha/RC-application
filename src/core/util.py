from logging import Formatter
from typing import Any

from .exceptions import AssignmentError

class LogCompressor(Formatter):
    """
    Custom formatter that truncates messages longer than a specified byte limit.
    """

    DEFAULT_MAX_BYTES: int = 256
    """
    Default maximum byte limit for message truncation.
    """
    TRUNCATION_SUFFIX: bytes = "...".encode()
    """
    Suffix added to truncated messages.
    """
    MINIMUM_REQUIRED_BYTES: int = 3
    """
    Minimum required byte limit for message truncation.
    """

    def __init__(self, fmt=None, datefmt=None, max_bytes: int = DEFAULT_MAX_BYTES):
        """
        Initializes the formatter with the specified format, date format, and maximum byte limit.

        Args:
            fmt: The format string for the formatter.
            datefmt: The date format string for the formatter.
            max_bytes: The maximum byte limit for message truncation.

        Raises:
            ValueError: If max_bytes is less than the minimum required bytes.
        """
        super().__init__(fmt, datefmt)
        if max_bytes < LogCompressor.MINIMUM_REQUIRED_BYTES:
            raise ValueError("Invalid number of maximum bytes; must be at least 3")
        self.max_bytes = max_bytes

    def format(self, record) -> str:
        """
        Formats the log record by truncating the message if it exceeds the byte limit.

        Args:
            record: The log record to format.

        Returns:
            str: The formatted log record.
        """
        msg = record.getMessage()
        msg_bytes = msg.encode()
        
        if len(msg_bytes) > self.max_bytes:
            # Truncate and add indicator.
            suffix_bytes = len(LogCompressor.TRUNCATION_SUFFIX)
            truncated_bytes = msg_bytes[:self.max_bytes - suffix_bytes] + LogCompressor.TRUNCATION_SUFFIX
            truncated_msg = truncated_bytes.decode()
            record.msg = truncated_msg
            # Clear args so getMessage() doesn't try to re-format.
            record.args = ()

        return super().format(record)

class Immutable:
    """
    A base class that enforces write-once immutability for its attributes.

    This class overrides `__setattr__` to ensure that attributes can only be
    set once (during initialization).
    Any attempt to modify an existing attribute will raise an exception.

    Usage:
        Inherit from this class to make your objects immutable after 
        their `__init__` method completes.

    Example:
        >>> class Point(Immutable):
        ...     def __init__(self, x, y):
        ...         self.x = x
        ...         self.y = y
        ...
        >>> p = Point(1, 2)
        >>> p.x
        1
        >>> p.x = 3
        Immutable Exception: Cannot modify 'x'.
    """

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Sets the value of an attribute only if it does not already exist.
        
        Raises:
            AssignmentError: If the attribute `name` already exists on the instance.
        """
        try:
            # Should throw AttributeError when initializing.
            _ = self.__getattribute__(name)
            # If the attribute already exists (was created by constructor),
            # then the immutability property tried to be violated.
            raise AssignmentError(f"Cannot modify '{name}'")
        except AttributeError:
            # If __getattribute__ raises AttributeError, the attribute is missing.
            # Therefore allow the construction of the object.
            super().__setattr__(name, value)

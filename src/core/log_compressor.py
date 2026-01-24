from logging import Formatter

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

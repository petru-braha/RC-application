from typing import Any, Callable
from functools import wraps
from urllib.parse import urlparse

from .config import TLS_ENFORCED
from .constants import EMPTY_STR, SCHEME_LIST
from .exceptions import AssignmentError
from .get_logger import get_logger

logger = get_logger(__name__)

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

def uninterruptible(callback: Callable) -> Callable:
    """
    Decorator to make a function uninterruptible.
    Catches system signals (like KeyboardInterrupt) and retries the execution,
    ensuring the operation completes unless a standard Exception occurs.
    """
    @wraps(callback)
    def wrapper(*args, **kwargs):
        while True:
            try:
                return callback(*args, **kwargs)
            except Exception:
                # Allow standard exceptions (ValueError, TypeError, etc.) to propagate.
                raise
            except BaseException as e:
                # Catch signals (KeyboardInterrupt, SystemExit) and retry.
                logger.error(f"func: {callback.__name__} interrupted by {e!r}. Retrying...")
    return wrapper

def process_redis_url(url: str, tls_enforced: bool = TLS_ENFORCED) -> tuple[str, str, str, str, str]:
    """
    Processes and extracts data from a Redis URL string.
    
    Format: redis[s]://[[username][:password]@][host][:port][/db-number]
    See more: https://docs.python.org/3/library/urllib.parse.html#url-parsing

    Args:
        url (str): A string representing the Redis connection URL.
    
    Returns:
        arr: A five-string tuple contaning the connection information.

    Raises:
        ValueError: For invalid URL scheme or malformed URL.
        ConnecterError: If the connection to the server fails.
    """
    logger.debug(f"Processing Redis URL: {url}.")
    parsed = urlparse(url)

    if parsed.scheme not in SCHEME_LIST:
        raise ValueError(f"Invalid url scheme: '{parsed.scheme}'")
    if tls_enforced and parsed.scheme == SCHEME_LIST[0]:
        raise ValueError("TLS is enforced, and an invalid scheme was provided.")

    host = parsed.hostname if parsed.hostname else EMPTY_STR
    port = str(parsed.port) if parsed.port else EMPTY_STR
    user = parsed.username if parsed.username else EMPTY_STR
    pasw = parsed.password if parsed.password else EMPTY_STR

    # Extraction of logical database index (the path segment).
    # Redis URLs typically use /0, /1, etc.
    db_idx = EMPTY_STR
    if parsed.path:
        # Strip leading slash, and check if the integer is valid.
        db_idx = parsed.path.lstrip('/')
        
    if db_idx != EMPTY_STR:
        try:
            int(db_idx)
        except ValueError:
            raise ValueError(
                f"Invalid database index: '{parsed.path}'; must be an integer"
            )
    
    # Do not log the password, sensitive data.
    logger.debug(f"Url connection details: host={host}, port={port}, user={user}, db={db_idx}")
    return (host, port, user, pasw, db_idx)

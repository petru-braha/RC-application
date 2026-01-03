from typing import Any
from urllib.parse import urlparse

from protocol import parser, encoder

from exceptions import AssignmentError
from constants import EMPTY_STR, SCHEME_LIST, ASCII_ENC

def join_cmd_argv(cmd: str, argv: list[str]) -> str:
    """
    Concatenates a command name and its arguments into a space-separated string.

    Returns:
        str: The formatted command string.
    """
    fragments = [cmd]
    fragments.extend(argv)
    return " ".join(fragments)

def process_redis_url(url: str) -> tuple:
    """
    Processes and extracts data from a Redis URL string (e.g., 'redis://user:password@host:port').
    
    Args:
        url: A string representing the Redis connection URL
        (format: redis[s]://[[username][:password]@][host][:port][/db-number]).
    
    Returns: A five-string tuple contaning the connection information.

    Raises:
        ValueError: If the URL scheme is not 'redis' or if the URL is malformed.
        ConnecterError: If the connection to the server fails.
    """
    parsed = urlparse(url)

    if parsed.scheme not in SCHEME_LIST:
        raise ValueError(f"Invalid URL scheme: '{parsed.scheme}'.")

    host = parsed.hostname if parsed.hostname else EMPTY_STR
    port = parsed.port if parsed.port else EMPTY_STR
    user = parsed.username if parsed.username else EMPTY_STR
    pasw = parsed.password if parsed.password else EMPTY_STR

    # Extraction of logical database index (the path segment).
    # Redis URLs typically use /0, /1, etc.
    db_idx = EMPTY_STR
    if parsed.path:
        try:
            # Strip leading slash and convert to int.
            db_idx = int(parsed.path.lstrip('/'))
        except ValueError:
            raise ValueError(
                f"Invalid database index: '{parsed.path}'. Must be an integer."
            )
    return (host, port, user, pasw, db_idx)

def process_input(input_str: str) -> bytes:
    cmd, argv = parser(input_str)
    # todo sanitizer?
    encoded = encoder(cmd, argv)
    return encoded.encode(ASCII_ENC)

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
            raise AssignmentError(f"Cannot modify '{name}'.")
        except AttributeError:
            # If __getattribute__ raises AttributeError, the attribute is missing.
            # Therefore allow the construction of the object.
            super().__setattr__(name, value)

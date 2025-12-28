from typing import Any

from protocol import parser, encoder

from exceptions import AssignmentError

def join_cmd_argv(cmd: str, argv: list[str]) -> str:
    """
    Concatenates a command name and its arguments into a space-separated string.

    Returns:
        str: The formatted command string.
    """
    fragments = [cmd]
    fragments.extend(argv)
    return " ".join(fragments)

def url_to_address(url: str) -> Address:
from urllib.parse import urlparse, unquote

class UrlConnection(Connection):
    """
    A specialized Connecter class that initializes via a Redis URL string.

    This class parses a standard Redis URL (e.g., 'redis://user:password@host:port/db')
    to extract connection parameters and passes them to the base Connecter logic.
    It supports authentication credentials and logical database selection.

    Supported formats:
        redis[s]://[[username][:password]@][host][:port][/db-number]
    """

    _SCHEME_LIST: tuple[str, str] = ("redis", "rediss")

    def __init__(self, url: str) -> None:
        """
        Parses the provided URL and initializes the Redis connection.

        Args:
            url: A string representing the Redis connection URL.

        Raises:
            ValueError: If the URL scheme is not 'redis' or if the URL is malformed.
            ConnecterError: If the connection to the server fails.
        """
        parsed = urlparse(url)

        if parsed.scheme not in UrlConnection._SCHEME_LIST:
            raise ValueError(
                f"Invalid URL scheme: '{parsed.scheme}'."
            )

        host = parsed.hostname
        port = parsed.port
        user = unquote(parsed.username) if parsed.username else None
        pasw = unquote(parsed.password) if parsed.password else None

        # Extraction of logical database index (the path segment).
        # Redis URLs typically use /0, /1, etc.
        db_idx = None
        if parsed.path:
            try:
                # Strip leading slash and convert to int.
                db_idx = int(parsed.path.lstrip('/'))
            except ValueError:
                raise ValueError(
                    f"Invalid database index: '{parsed.path}'. Must be an integer."
                )

        super().__init__(host, port, user, pasw, db_idx)    

def prepare_cmd(cmd: str) -> bytes:
    cmd, argv = parser(cmd)
    encoded = encoder(cmd, argv)
    return encoded.encode("ascii")

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

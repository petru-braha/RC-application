from urllib.parse import urlparse, unquote

from .identification import Identification

class Connection(Identification):
    """
    """

    DEFAULT_DB: int = 0
    """
    Default logical database of a Redis instance.
    """

    # Internally host and port will be converted into an Address object.
    # Here host and port are kept as parameterss,
    # since clients might be intersted in typing them manually, can not generalize them.
    def __init__(self,
                 host: str | None = None,
                 port: str | None = None,
                 user: str | None = None,
                 pasw: str | None = None,
                 db_idx: str | None = None) -> None:
        super().__init__(host, port, user, pasw)
        self.db_idx = Connection.DEFAULT_DB if db_idx == None else db_idx

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

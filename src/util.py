from urllib.parse import urlparse

from core.config import Config
from core.constants import EMPTY_STR, SCHEME_LIST, ASCII_ENC
from protocol import parser, encoder, Output

logger = Config.get_logger(__name__)

def process_input(input_str: str) -> bytes:
    """
    Processes the input string by parsing it into a command and arguments,
    encoding it, and returning the encoded bytes.
    
    Args:
        input_str (str): A string representing the input to be processed.
    
    Returns:
        bytes: The encoded bytes of the input string.

    Raises:
        ValueError: If the input string is invalid.
    """
    logger.debug(f"Processing input: {input_str}.")
    
    try:
        cmd, argv = parser(input_str)
    except Exception as e:
        raise ValueError(f"Invalid input {input_str}. {e}.")
    logger.debug(f"Parsed command: {cmd}, arguments: {argv}.")
    
    # todo sanitizer
    
    encoded = encoder(cmd, argv)
    logger.debug(f"Encoded command: {encoded}.")
    
    return encoded.encode(ASCII_ENC)

def process_output(output: Output) -> str:
    pass

def process_redis_url(url: str) -> tuple[str, str, str, str, str]:
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
    logger.debug(f"Processing Redis URL: {url}.")
    parsed = urlparse(url)

    if parsed.scheme not in SCHEME_LIST:
        raise ValueError(f"Invalid URL scheme: '{parsed.scheme}'")

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
                f"Invalid database index: '{parsed.path}'. Must be an integer"
            )
    
    # Do not log the password, sensitive data.
    logger.debug(f"Url connection details: host={host}, port={port}, user={user}, db={db_idx}")
    return (host, port, user, pasw, db_idx)

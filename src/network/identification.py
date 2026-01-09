from core.config import get_logger
from core.constants import EMPTY_STR, RespVer
from core.structs import Address

from .transmitter import Transmitter
from .util import join_cmd_argv

logger = get_logger(__name__)

class Identification(Transmitter):
    """
    Manages the initial identification phase of the Redis protocol connection.
    Handles the HELLO handshake and authentication details.
    """
    
    DEFAULT_HOST: str = "localhost"
    """
    Default host used for Redis servers.
    """
    DEFAULT_PORT: str = "6379"
    """
    Default port used for Redis servers.
    """
    DEFAULT_USER: str = "default"
    """
    Default ACL user.
    """

    HELLO_CMD: str = "HELLO"
    """
    First command ever sent to a newly established connection.
    Negotiates the protocol, and authentificate the client.
    """
    _AUTH_ARG: str = "AUTH"
    """ 
    The authentication argument for the HELLO command.
    """
    
    def __init__(self, host: str, port: str, user: str, pasw: str) -> None:
        """
        Saves the initial username and password a client tried to connect with.
        If the initial hello command does not succed,
        these information are necessary to recover from errors and retry authentication.

        Note: Keep in mind that the initial username and password are mutable.
        """
        host = Identification.DEFAULT_HOST if host == EMPTY_STR else host
        port = Identification.DEFAULT_PORT if port == EMPTY_STR else port
        addr = Address(host, port)
        
        initial_user = Identification.DEFAULT_USER if user == EMPTY_STR else user
        initial_pasw = pasw
        
        super().__init__(addr)
        self.say_hello(initial_user, initial_pasw)
        self.initial_user = initial_user
        self.initial_pasw = initial_pasw
    
    def say_hello(self, user: str, pasw: str, protver: int = RespVer.RESP3) -> None:
        """
        Queues the HELLO command with the specified authentication credentials and protocol version.

        Args:
            user (str): The username for authentication.
            pasw (str): The password for authentication.
            protver (int): The RESP protocol version to negotiate (default is 3).

        Raises:
            ValueError: If an invalid protocol version is specified.
        """
        protver = RespVer(protver)
        argv = [str(protver), Identification._AUTH_ARG, user]
        if pasw != EMPTY_STR:
            argv.append(pasw)
        
        logger.info(f"Queueing HELLO handshake for user '{user}' (Protocol {protver}).")
        pending_input = join_cmd_argv(Identification.HELLO_CMD, argv)
        self.sender.add_pending(pending_input)

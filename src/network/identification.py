from protocol.cmds.patterns.constants import AUTH_ARG

from constants import EMPTY_STR
from structs import Address
from util import join_cmd_argv

from .transport import Archiver, Receiver, Sender

class Identification(Archiver, Receiver, Sender):
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

    _HELLO_CMD: str = "HELLO"
    """
    First command ever sent to a newly established connection.
    Negotiates the protocol, and authentificate the client.
    """
    _RESP3: str = "3"
    """
    The newest available RESP protocol version. 
    """
    _RESP2: str = "2"
    """
    The stable version of RESP.
    """
    
    def __init__(self, host: str, port: str, user: str, pasw: str) -> None:
        """
        Saves the initial username and password a client tried to connect with.
        If the initial hello command does not succed,
        these information are necessary to recover from errors and retry authentication.

        Note: Keep in mind that the initial username and password are mutable.
        """
        host = Identification.DEFAULT_HOST if host == None else host
        port = Identification.DEFAULT_PORT if port == None else port
        addr = Address(host, port)

        initial_user = Identification.DEFAULT_USER if user == None else user
        initial_pasw = EMPTY_STR if pasw == None else pasw

        Archiver.__init__(self)
        Receiver.__init__(self, addr)
        Sender.__init__(self, addr)
        self.say_hello(initial_user, initial_pasw)
        self.initial_user = initial_user
        self.initial_pasw = initial_pasw
    
    def say_hello(self, user: str, pasw: str, protver: str = _RESP3) -> None:
        """
        Queues the HELLO command with the specified authentication credentials and protocol version.

        Parameters:
            user (str): The username for authentication.
            pasw (str): The password for authentication.
            protver (str): The RESP protocol version to negotiate (default is 3).
        """
        argv = [protver, AUTH_ARG.pattern, user, pasw]
        pending_input = join_cmd_argv(Identification._HELLO_CMD, argv)
        self.add_pending(pending_input)

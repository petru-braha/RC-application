from constants import EMPTY_STR
from structs import Address

from .sock import Sock

class Identification(Sock):
    """
    Attributes:
        addr (obj): The address object consisting of the host and port.
        user (str): The username of the client authentificated.
        pasw (str): The password of the same client.
        sock (obj): The socket object
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

    def __init__(self,
                 host: str | None = None,
                 port: str | None = None,
                 user: str | None = None,
                 pasw: str | None = None) -> None:
        host = Identification.DEFAULT_HOST if host == None else host
        port = Identification.DEFAULT_PORT if port == None else port
        addr = Address(host, port)
        super().__init__(addr)
        
        user = Identification.DEFAULT_USER if user == None else user
        self.user = user
        self.pasw = EMPTY_STR if pasw == None else pasw

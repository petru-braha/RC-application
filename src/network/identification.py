from constants import EMPTY_STR
from structs import Address

from .transport import Archiver, Receiver, Sender

class Identification(Archiver, Receiver, Sender):
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

        user = Identification.DEFAULT_USER if user == None else user
        pasw = EMPTY_STR if pasw == None else pasw

        Archiver.__init__(self)
        Receiver.__init__(self, addr)
        Sender.__init__(self, addr)
    
    def say_hello(self):
        # todo Implementation of sending HELLO command
        pass


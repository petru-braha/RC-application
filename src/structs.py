from dataclasses import dataclass

from output import Output

@dataclass(frozen=True)
class Address:
    """
    Server address composed of host and port.
    """
    host: str
    port: str

@dataclass()
class Dialogue:
    """
    Request-response pair for a connection.
    """
    cmd: str
    output: Output

History = list[Dialogue]
"""
Chat/socket connection history of requests and responses.
"""

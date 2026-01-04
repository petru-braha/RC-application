from dataclasses import dataclass

@dataclass(frozen=True)
class Address:
    """
    Server address composed of host and port.
    """
    host: str
    port: str

    def __str__(self) -> str:
        return f"{self.host}:{self.port}"

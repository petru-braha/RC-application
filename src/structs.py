from dataclasses import dataclass

from frontend import Chat, ConnectionBox

from output import Output

@dataclass(frozen=True)
class Address:
    """
    Server address composed of host and port.
    """
    host: str
    port: str

    def __str__(self) -> str:
        return f"{self.host}:{self.port}"

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

class ConnectionPresentation:
    """
    Consists of the Connection button
    """

    def __init__(self, chat: Chat, connection_box: ConnectionBox) -> None:
        self.chat = chat
        self.connection_box = connection_box

#              connection_text: str,
#              on_select: Callable,
#              on_close: Callable,
#              chat_frame: ChatFrame, on_remove: Callable
#
    # Operator.close(self.connection)
    #        self.history_box.hide()
    #        on_remove(self)
    # todo dispaly reset

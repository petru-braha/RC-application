from typing import Callable

from network import Connection

from .members import ConnectionBox, HistoryBox

class ConnectionContext:
    def __init__(self, connection: Connection, on_remove: Callable):
        self._on_remove = on_remove
        self.connection = connection
        self.history_box = HistoryBox()
        self.connection_box = ConnectionBox(
            str(connection.addr),
            on_click=self.history_box.show,
            on_close=self.on_close)

    def on_close(self):
        self.connection.close()
        self._on_remove(self)

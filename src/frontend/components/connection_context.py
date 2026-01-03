import flet as ft

from typing import Callable

from core import Operator
from frontend import HistoryContext
from network import Connection

from .members import ConnectionBox, HistoryBox

class ConnectionContext:
    def __init__(self, connection: Connection, history_context: HistoryContext, on_remove: Callable) -> None:
        self.history_box = HistoryBox(connection, history_context)
        
        def on_close():
            Operator.close(self.connection)
            self.history_box.hide()
            on_remove(self)
        
        self.connection_box = ConnectionBox(
            connection.addr,
            on_click=self.history_box.show,
            on_close=self.on_close)

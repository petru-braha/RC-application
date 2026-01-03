import flet as ft

from frontend import HistoryContext
from network import Connection

from .connection_context import ConnectionContext

class ConnectionList(ft.Column):
    def __init__(self, history_context: HistoryContext) -> None:
        self.history_context = history_context
        self.list_view = ft.ListView(
            expand=True,
            spacing=10,
            padding=10,
            auto_scroll=True
        )
        super().__init__(
            [self.list_view],
            expand=True,
        )

    def insert_connection(self, connection: Connection) -> None:
        connection_context = ConnectionContext(
            connection,
            history_context=self.history_context,
            on_remove=self.remove_connection)
        self.list_view.controls.append(connection_context.connection_box)
        self.list_view.update()

    def remove_connection(self, connection_context: ConnectionContext) -> None:
        assert connection_context in self.list_view.controls
        self.list_view.controls.remove(connection_context)
        
        if not self.list_view.controls:
            self.history_context.reset()
        else:
            first_connection = self.list_view[0]
            assert isinstance(first_connection, ConnectionContext)
            first_connection.connection_box.on_click()
        
        self.list_view.update()

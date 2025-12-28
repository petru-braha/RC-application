import flet as ft

from network import Connection

from .members import ConnectionBox

class ConnectionList(ft.Column):
    def __init__(self):
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

    def insert_connection(self, connection: Connection):
        box = ConnectionBox(connection, self.remove_connection)
        self.list_view.controls.append(box)
        self.list_view.update()

    def remove_connection(self, connection_box: ConnectionBox):
        assert connection_box in self.list_view.controls
        self.list_view.controls.remove(connection_box)
        self.list_view.update()

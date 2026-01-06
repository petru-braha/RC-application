import flet as ft

from .members import ConnectionBox

class Agenda(ft.Column):

    def __init__(self) -> None:
        self.list_view = ft.ListView(
            expand=True,
            spacing=10,
            padding=10,
            auto_scroll=True
        )
        super().__init__(
            controls=[self.list_view],
            expand=True,
        )

    def add_box(self, connection_box: ConnectionBox) -> None:
        self.list_view.controls.append(connection_box)
        self.update()

    def rem_box(self, connection_box: ConnectionBox) -> None:
        """
        Remove first occurrence of presentation.

        Raises:
            ValueError: If the value is not present.
        """
        self.list_view.controls.remove(connection_box)
        self.update()

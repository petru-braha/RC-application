import flet as ft

from .members import ConnectionBox

class Agenda(ft.Column):
    def __init__(self) -> None:
        controls = [ft.ListView(
            expand=True,
            spacing=10,
            padding=10,
            auto_scroll=True
        )]
        super().__init__(
            controls=controls,
            expand=True,
        )

    def insert(self, connection_box: ConnectionBox) -> None:
        self.controls.append(connection_box)
        self.update()

    def remove(self, connection_box: ConnectionBox) -> None:
        """
        Remove first occurrence of presentation.

        Raises:
            ValueError: If the value is not present.
        """
        self.controls.remove(connection_box)
        self.update()

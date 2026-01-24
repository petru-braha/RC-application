import flet as ft

from .members import ConnectionBox

class Agenda(ft.Column):
    """
    A column container that holds and displays a list of connection boxes.
    """

    def __init__(self) -> None:
        """
        Initialize the Agenda with a scrollable list view.
        """
        list_view = ft.ListView(
            expand=True,
            spacing=10,
            padding=10,
            auto_scroll=True,
            scroll=ft.ScrollMode.AUTO,
        )
        super().__init__(
            controls=[list_view],
            expand=True,
        )
        self.list_view = list_view

    def add_box(self, connection_box: ConnectionBox) -> None:
        """
        Adds a connection box to the agenda.
        
        Note: this method is forwarded to the connection creation handlers.

        Args:
            connection_box (obj): The connection box to add.
        """
        self.list_view.controls.append(connection_box)
        self.update()

    def rem_box(self, connection_box: ConnectionBox) -> None:
        """
        Remove first occurrence of presentation.
        
        Note: this method is forwarded to the connection removal handlers.

        Args:
            connection_box (obj): The connection box to remove.

        Raises:
            ValueError: If the value is not present.
        """
        self.list_view.controls.remove(connection_box)
        self.update()

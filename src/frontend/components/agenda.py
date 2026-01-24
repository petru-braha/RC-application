import flet as ft

from .conn_box import ConnBox

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
        self.conn_boxes = list_view

    def add_box(self, conn_box: ConnBox) -> None:
        """
        Adds a connection box to the agenda.
        
        Note: this method is forwarded to the connection creation handlers.

        Args:
            conn_box (obj): The connection box to add.
        """
        self.conn_boxes.controls.append(conn_box)
        self.update()

    def rem_box(self, conn_box: ConnBox) -> None:
        """
        Remove first occurrence of presentation.
        
        Note: this method is forwarded to the connection removal handlers.

        Args:
            conn_box (obj): The connection box to remove.

        Raises:
            ValueError: If the value is not present.
        """
        self.conn_boxes.controls.remove(conn_box)
        self.update()

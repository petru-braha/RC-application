import flet as ft
from typing import Callable

from .components import ConnBox

class AgendaFrame(ft.Container):
    """
    Groups the agenda and the connect button under a unitary panel.
    """

    def __init__(self, show_modal_callback: Callable) -> None:
        conn_boxes = ft.ListView(
            expand=True,
            spacing=10,
            padding=10,
            auto_scroll=True,
            scroll=ft.ScrollMode.AUTO,
        )
        
        connect_btn = ft.Button("Connect", on_click=show_modal_callback)
        
        content_controls = [
            ft.Column(
                controls=[conn_boxes],
                expand=True
            ),
            ft.Divider(),
            ft.Row([connect_btn], alignment=ft.MainAxisAlignment.CENTER)
        ]
        content = ft.Column(
            controls=content_controls,
            expand=True
        )
        super().__init__(
            content=content,
            width=250,
            bgcolor=ft.Colors.BLUE_GREY_900,
            padding=10,
        )
        self.conn_boxes = conn_boxes
    
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

import flet as ft
from typing import Callable

class ConnBox(ft.Container):
    """
    A visual representation of an active connection in the agenda.
    Allows selection and closing of the connection.
    """

    def __init__(self, text: str, on_click: Callable, on_close: Callable) -> None:
        content=ft.Stack([
            ft.Text(text,
                left=5, 
                bottom=5, 
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD),
            # Close button of the connection.
            ft.IconButton(
                icon=ft.Icons.CLOSE,
                icon_color=ft.Colors.WHITE_54,
                icon_size=20,
                right=0,
                top=0,
                on_click=on_close
            )
        ])
        super().__init__(
            content=content,
            width=200,
            height=80,
            bgcolor=ft.Colors.BLUE_GREY_700,
            border_radius=5,
            on_click=on_click,
            ink=True
        )

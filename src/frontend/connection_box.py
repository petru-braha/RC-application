import flet as ft

from src.network import Connection

class ConnectionBox(ft.Container):

    left_panel: ft.Column

    def __init__(self, connection: Connection) -> None:
        
        display_text = f"{connection.addr.host}:{connection.addr.port}"
        
        def remove_connection(e):
            ConnectionBox.left_panel.controls.remove(self)
            ConnectionBox.left_panel.update()

        content=ft.Stack([
            ft.Text(display_text,
                left=5, 
                bottom=5, 
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD),
            ft.IconButton(
                icon=ft.Icons.CLOSE,
                icon_color=ft.Colors.WHITE_54,
                icon_size=20,
                right=0,
                top=0,
                on_click=remove_connection
            )
        ])
        
        super().__init__(
            content=content,
            width=200,
            height=80,
            bgcolor=ft.Colors.BLUE_GREY_700,
            border_radius=5,
            on_click=lambda e: self.on_select(conn_info)
        )
        
        self.connection = connection
        ConnectionBox.left_panel.controls.insert(0, self)
        ConnectionBox.left_panel.update()

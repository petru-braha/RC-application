import flet as ft
from typing import Callable

class ConnectionList(ft.Column):
    def __init__(self, on_select: Callable):
        super().__init__()
        self.on_select = on_select
        self.connections_data = [] # List of dicts or objects
        self.list_view = ft.ListView(
            expand=True,
            spacing=10,
            padding=10,
            auto_scroll=True
        )
        self.controls = [self.list_view]
        self.expand = True

    def add_connection(self, conn_info: dict):
        # conn_info: {"host": ..., "port": ..., ...}
        self.connections_data.insert(0, conn_info)
        
        # Create visual representation
        # "each connection will be represented by a rectangle. the host and port (the adddr) will be visible on it in the lower left of the rectangle."
        
        display_text = f"{conn_info.get('host', 'unknown')}:{conn_info.get('port', '6379')}"
        
        def remove_connection(e):
            self.list_view.controls.remove(rect)
            self.update()

        rect = ft.Container(
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
            ]),
            width=200, 
            height=80,
            bgcolor=ft.Colors.BLUE_GREY_700,
            border_radius=5,
            on_click=lambda e: self.on_select(conn_info)
        )
        
        # Insert at top
        self.list_view.controls.append(rect)
        self.update()

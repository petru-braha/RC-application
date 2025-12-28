import flet as ft

from network import Connection
from app_state import AppState
from ...state import FrontendState

class ConnectionBox(ft.Container):

    def __init__(self, connection: Connection, on_remove) -> None:
        
        display_text = f"{connection.addr.host}:{connection.addr.port}"
        
        def remove_connection(e):
            on_remove(self)

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

        def on_click(e):
            # Try/Except to handle potential missing keys if connection validation is mocked
            try:
                hist = AppState._sock_hist_dict.get(connection)
                if hist and FrontendState.chat_history_widget:
                    FrontendState.chat_history_widget.set_hist(hist)
                    FrontendState.chat_history_widget.update()
            except Exception as e:
                print(f"Error accessing history: {e}")
        
        super().__init__(
            content=content,
            width=200,
            height=80,
            bgcolor=ft.Colors.BLUE_GREY_700,
            border_radius=5,
            on_click=on_click
        )
        
        self.connection = connection

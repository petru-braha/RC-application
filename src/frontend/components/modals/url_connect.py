import flet as ft
from typing import Callable

from frontend import ConnectionModal, PresenceChangeable

class UrlConnect(ft.AlertDialog, PresenceChangeable):
    def __init__(self, on_manual: Callable, on_continue: Callable):
        
        self.url_input = ft.TextField(
            hint_text="redis://user:pass@host:port/db", 
            text_align=ft.TextAlign.CENTER
        )
    
        prompt = ft.Text("Paste the connection url", text_align=ft.TextAlign.CENTER)
        content = ft.Container(
            width=400,
            height=300,
            content=ft.Column(
                [
                    ft.Container(height=20), # Spacer
                    ft.Row([prompt], alignment=ft.MainAxisAlignment.CENTER),
                    self.url_input,
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        super().__init__(
            content=content,
            actions=[
                ft.IconButton(ft.Icons.CLOSE, on_click=self.hide, tooltip="Close"),
                ft.Button("Manual connection info", on_click=on_manual),
                ft.Button("Continue", on_click=on_continue),
            ]
        )

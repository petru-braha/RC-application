import flet as ft
from typing import Callable

from frontend import ConnectionModal, PresenceChangeable

class ManualConnect(ft.AlertDialog, PresenceChangeable):
    def __init__(self, on_back: Callable, on_continue: Callable):
        
        self.host_input = ft.TextField(hint_text="Host")
        self.port_input = ft.TextField(hint_text="Port")
        self.user_input = ft.TextField(hint_text="Username")
        self.pass_input = ft.TextField(
            hint_text="Password", 
            password=True, 
            can_reveal_password=True
        )
        self.db_input = ft.TextField(hint_text="Database Index")
    
        prompt = ft.Text("Paste manual connection info", text_align=ft.TextAlign.CENTER)
        content = ft.Container(
            width=400,
            height=500,
            content=ft.Column(
                [
                    ft.Row([prompt], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.host_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.port_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.user_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.pass_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.db_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=10),
                ],
                scroll=ft.ScrollMode.AUTO
            )
        )

        super().__init__(
            content=content,
            actions=[
                ft.IconButton(ft.Icons.CLOSE, on_click=self.hide, tooltip="Close"),
                ft.Button("Continue", on_click=on_continue),
                ft.Button("Back", on_click=on_back),
            ]
        )

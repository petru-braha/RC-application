import flet as ft
from typing import Callable

from .interfaces import ModalBase

class ManualConnect(ModalBase):
    def __init__(self, on_continue: Callable, switch_btn: ft.Control, close_btn: ft.Control):
        super().__init__()
        self._on_continue_callback = on_continue
        
        self.host_input = ft.TextField(hint_text="Host")
        self.port_input = ft.TextField(hint_text="Port")
        self.user_input = ft.TextField(hint_text="Username")
        self.pass_input = ft.TextField(
            hint_text="Password", 
            password=True, 
            can_reveal_password=True
        )
        self.db_input = ft.TextField(hint_text="Database Index (0-15)")

        header = ft.Row([ft.Container(expand=True), close_btn], alignment=ft.MainAxisAlignment.END)
        prompt = ft.Text("Paste manual connection info", text_align=ft.TextAlign.CENTER)
        continue_btn = ft.Button("Continue", on_click=self.on_process_manual)
        self.content = ft.Column(
            [
                header,
                ft.Column([
                    ft.Row([prompt], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([switch_btn], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.host_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.port_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.user_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.pass_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.db_input], alignment=ft.MainAxisAlignment.CENTER),
                ], expand=True, scroll=ft.ScrollMode.AUTO),
                ft.Container(height=10),
                # Footer
                ft.Divider(),
                ft.Row([continue_btn], alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def on_process_manual(self, e) -> None:
        host = self.host_input.value
        port = self.port_input.value
        user = self.user_input.value
        pasw = self.pass_input.value
        db_idx = self.db_input.value
        connection_data = (host, port, user, pasw, db_idx)
        self._on_continue_callback(connection_data)

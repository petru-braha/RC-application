import flet as ft
from typing import Callable

from frontend import ConnectionModal

from util import process_redis_url

class UrlMode(ConnectionModal):
    def __init__(self, on_agenda_insert: Callable, on_agenda_remove: Callable, on_chat_insert: Callable):
        super().__init__(on_agenda_insert, on_agenda_remove, on_chat_insert)
        
        self.url_input = ft.TextField(
            hint_text="redis://user:pass@host:port/db", 
            text_align=ft.TextAlign.CENTER
        )
    
    def set_url_mode(self):
        close_btn = ft.IconButton(ft.Icons.CLOSE, on_click=self.hide, tooltip="Close")
        manual_btn = ft.Button("Manual connection info", on_click=lambda e: self.set_manual_mode())
        continue_btn = ft.Button("Continue", on_click=self.on_url_continue)
        prompt = ft.Text("Paste the connection url", text_align=ft.TextAlign.CENTER)

        header = ft.Row([ft.Container(expand=True), close_btn], alignment=ft.MainAxisAlignment.END)

        self.content = ft.Container(
            width=400,
            height=300,
            content=ft.Column(
                [
                    header,
                    ft.Container(height=20), # Spacer
                    ft.Row([manual_btn], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([prompt], alignment=ft.MainAxisAlignment.CENTER),
                    self.url_input,
                    ft.Row([continue_btn], alignment=ft.MainAxisAlignment.CENTER),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        self.update()
    
    def on_url_continue(self, e) -> None:
        url = self.url_input.value
        components = process_redis_url(url)
        self.on_continue(components)

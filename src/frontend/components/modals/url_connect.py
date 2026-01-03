import flet as ft
from typing import Callable

from util import process_redis_url

class UrlConnect(ft.Container):
    def __init__(self, on_continue: Callable):
        super().__init__()
        
        self.url_input = ft.TextField(
            hint_text="redis://user:pass@host:port/db", 
            text_align=ft.TextAlign.CENTER
        )
    
        prompt = ft.Text("Paste the connection url", text_align=ft.TextAlign.CENTER)
        continue_btn = ft.Button("Continue", on_click=self.on_process_url)
        self._on_continue_callback = on_continue

        self.content = ft.Column(
            [
                ft.Container(height=20), # Spacer
                ft.Row([prompt], alignment=ft.MainAxisAlignment.CENTER),
                self.url_input,
                ft.Container(height=10),
                ft.Row([continue_btn], alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.width = 400
        self.height = 300

    def on_process_url(self, e) -> None:
        url = self.url_input.value
        try:
            # Assuming process_redis_url returns the tuple connection_data
            components = process_redis_url(url)
            self._on_continue_callback(components)
        except Exception as ex:
            # Handle error (maybe show snackbar? but we don't have page access easily unless added)
            print(f"Error processing URL: {ex}")


import flet as ft
from typing import Callable

from core import get_logger
from util import process_redis_url

from .interfaces import ModalBase

logger = get_logger(__name__)

class UrlConnect(ModalBase):
    def __init__(self, on_continue: Callable, switch_btn: ft.Button, close_btn: ft.Button):
        super().__init__()
        self._on_continue_callback = on_continue
        
        self.url_input = ft.TextField(
            hint_text="redis://user:pass@host:port/db", 
            text_align=ft.TextAlign.CENTER,
        )
        
        header = ft.Row([ft.Container(expand=True), close_btn], alignment=ft.MainAxisAlignment.END)
        prompt = ft.Text("Paste the connection url", text_align=ft.TextAlign.CENTER)
        continue_btn = ft.Button("Continue", on_click=self.on_process_url)
        self.content = ft.Column(
            [
                header,
                ft.Column([
                    ft.Container(height=20),
                    ft.Row([prompt], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([switch_btn], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.url_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=10),
                ], expand=True, scroll=ft.ScrollMode.AUTO),
                # Footer.
                ft.Divider(),
                ft.Row([continue_btn],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.START)
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def on_process_url(self, e) -> None:
        url = self.url_input.value
        self.url_input.value = ""
        try:
            components = process_redis_url(url)
        except ValueError as err:
            logger.error(f"Invalid url, {err}.")
            return
        self._on_continue_callback(components)

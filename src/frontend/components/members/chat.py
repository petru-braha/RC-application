import flet as ft
from typing import Callable

from core import get_logger

from .interfaces import PresenceChangeable

logger = get_logger(__name__)

class Chat(ft.Container, PresenceChangeable):
    def __init__(self, text: str, on_enter: Callable[[str], None]) -> None:
        self._on_enter = on_enter
        self.history_box = ft.ListView(
            expand=True,
            auto_scroll=True,
            spacing=10,
            scroll=ft.ScrollMode.ALWAYS,
        )
        
        self.cmd_input = ft.TextField(
            hint_text="Type a command.",
            on_submit=self.on_submit)
        
        header = ft.Container(
            content=ft.Row(
                [
                    ft.Text(text, 
                        color=ft.Colors.WHITE, 
                        selectable=True,
                        weight=ft.FontWeight.BOLD
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            bgcolor=ft.Colors.BLUE_GREY_700,
            padding=10,
            border_radius=5,
        )
        content = ft.Column([
                header,
                self.history_box,
                ft.Divider(),
                ft.Row([self.cmd_input], alignment=ft.MainAxisAlignment.CENTER)
            ],
            expand=True
        )

        super().__init__(
            content=content,
            bgcolor=ft.Colors.BLUE_GREY_900,
            padding=10,
            expand=True,
        )

    def on_submit(self, e) -> None:
        req = self.cmd_input.value
        if not req:
            return

        logger.debug(f"Processing request: {req}.")
        self._on_enter(req)
        
        self.cmd_input.value = ""
        self.cmd_input.focus()
        
        bubble = self._create_client_bubble(req)
        self.history_box.controls.append(bubble)
        
        self.history_box.update()

    def on_response(self, res: str) -> None:
        """
        Called by reactor.
        """
        logger.debug(f"Processing response: {res}.")
        bubble = self._create_server_bubble(res)
        self.history_box.controls.append(bubble)
        self.update()

    def _create_client_bubble(self, text: str) -> ft.Row:
        return ft.Row(
            [
                ft.Container(
                    content=ft.Text(text, color=ft.Colors.WHITE, selectable=True),
                    padding=10,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE_600,
                    width=400,
                    ink=True
                )
            ],
            alignment=ft.MainAxisAlignment.END,
        )

    def _create_server_bubble(self, text: str) -> ft.Row:
        return ft.Row(
            [
                ft.Container(
                    content=ft.Text(text, color=ft.Colors.WHITE, selectable=True),
                    padding=10,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE_GREY_700,
                    width=400,
                    ink=True
                )
            ],
            alignment=ft.MainAxisAlignment.START,
        )

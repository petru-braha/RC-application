import flet as ft
from typing import Callable

from frontend import PresenceChangeable

class Chat(ft.Container, PresenceChangeable):
    def __init__(self, on_enter: Callable[[str], None]) -> None:
        self._on_enter = on_enter
        self.history_box = ft.ListView(
            expand=True,
            auto_scroll=True,
            scroll=ft.ScrollMode.ALWAYS,
        )
        
        self.cmd_input = ft.TextField(
            hint_text="Type a command.",
            on_submit=self.on_submit)
        
        content = ft.Column([
                self.history_box,
                ft.Divider(),
                ft.Row([self.cmd_input], alignment=ft.MainAxisAlignment.CENTER)
            ],
            expand=True
        )

        super().__init__(
            content=content,
            bgcolor=ft.Colors.BLUE_GREY_800,
            padding=10,
            expand=True,
        )

    def on_submit(self) -> None:
        request = self.cmd_input.value
        self._on_enter(request)
        to_display = ft.Text(request)
        self.history_box.controls.append(to_display)
        self.history_box.update()

    def on_response(self, res: str) -> None:
        """
        Called by reactor.
        """
        to_display = ft.Text(res)
        self.history_box.controls.append(to_display)
        self.update()

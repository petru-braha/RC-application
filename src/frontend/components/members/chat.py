import flet as ft
from typing import Callable

import core

from .interfaces import PresenceChangeable

logger = core.get_logger(__name__)

class Chat(ft.Container, PresenceChangeable):
    """
    A chat Interface container that displays the command history in a request-response format.
    """

    CLEAR_CMD: str = "CLEAR"
    """
    Client-side command used to clear the visual chat history.
    """

    def __init__(self, text: str, on_enter: Callable[[str], None]) -> None:
        """
        Initialize the Chat interface.

        Args:
            text (str): The initial text to display in the header (e.g. connection address).
            on_enter (lambda): Callback function to handle command submission.
        """
        cmd_input = ft.TextField(
            hint_text="Type a command.",
            autofocus=True,
            on_submit=self.on_submit)
        
        history_box = ft.ListView(
            expand=True,
            auto_scroll=True,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )
        
        header = ft.Container(
            content=ft.Row([
                ft.Text(text, 
                    color=ft.Colors.WHITE, 
                    selectable=True,
                    weight=ft.FontWeight.BOLD)],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            bgcolor=ft.Colors.BLUE_GREY_700,
            padding=10,
            border_radius=5,
        )
        content = ft.Column([
            header,
            history_box,
            ft.Divider(),
            ft.Row([cmd_input], alignment=ft.MainAxisAlignment.CENTER)],
            expand=True
        )
        super().__init__(
            content=content,
            bgcolor=ft.Colors.BLUE_GREY_900,
            padding=10,
            expand=True,
        )
        self._on_enter = on_enter
        self.cmd_input = cmd_input
        self.history_box = history_box

    async def on_submit(self, event) -> None:
        """
        Handles the submission of a new command from the input field.

        Args:
            event (obj): The event object.
        """
        req = self.cmd_input.value
        if not req:
            return
        
        self.cmd_input.value = ""
        await self.cmd_input.focus()
        
        if req.upper() == Chat.CLEAR_CMD:
            self.history_box.controls.clear()
            logger.debug("Cleaned chat history.")
            return

        logger.debug(f"Frontend printing of the request: {req}.")
        self._on_enter(req)
        bubble = self._add_msg_bubble(req, ft.MainAxisAlignment.END, ft.Colors.BLUE_600)
        self.history_box.controls.append(bubble)
        logger.debug("Request printed.")

    async def add_res(self, res: str) -> None:
        """
        Adds a response to the chat history box automaticallly when it is ready.

        Args:
            res (str): The response string from the server.
        """
        logger.debug(f"Frontend printing of the response: {res}.")

        bubble = self._add_msg_bubble(res, ft.MainAxisAlignment.START, ft.Colors.BLUE_GREY_700)
        self.history_box.controls.append(bubble)
        self.history_box.update()
        
        logger.debug("Response printed.")

    def _add_msg_bubble(self, text: str, alignment: ft.MainAxisAlignment, bgcolor: ft.Colors) -> ft.Row:
        """
        Creates a message bubble for client requests or server responses.

        Args:
            text (str): The request text.
            alignment (obj): The alignment of the message bubble.
                             The requests are aligned to the right,
                             and the responses to the left.
            bgcolor (obj): The background color of the message bubble.

        Returns:
            ft.Row: The formatted row containing the message bubble.
        """
        return ft.Row([
            ft.Container(
                content=ft.Text(text, color=ft.Colors.WHITE, selectable=True),
                padding=10,
                border_radius=10,
                bgcolor=bgcolor,
                width=400,
                ink=True
            )],
            alignment=alignment,
        )

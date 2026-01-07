import flet as ft

from .members import Chat

class ChatFrame(ft.Container):
    """
    Predefined frame to encapsulate the chat history boxes.

    Displays a standard default message.
    """

    _EMPTY_LEN: int = 1
    """
    Number of layers when there are no connections.
    """

    def __init__(self) -> None:
        default_layer=ft.Column([
            ft.Text("RC-application - a multi-connection Redis client.\n"
                    "Press \"Connect\" to get started.",
                size=20, 
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.LEFT
            )],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    
        super().__init__(
            content=default_layer,
            expand=True
        )
        self.default_layer = default_layer
    
    def sel_chat(self, chat: Chat) -> None:
        self.content = chat
        self.update()

    def rem_chat(self, chat: Chat) -> None:
        self.content = self.default_layer
        self.update()

import flet as ft

from .members import Chat

class ChatFrame(ft.Stack):
    """
    Predefined frame to encapsulate the chat history boxes.

    Displays a standard default message.
    """

    def __init__(self) -> None:
        default_layer=ft.Column([
            ft.Text("Connect to a Redis server.", 
                size=20, 
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            )],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    
        super().__init__(
            controls=[default_layer],
            expand=True
        )
        self.default_layer = default_layer

    def reset(self) -> None:
        """
        Called when all connections are removed.
        """
        self.controls = [self.default_layer]
        self.update()

    def set_chat(self, chat: Chat) -> None:
        self.controls = [chat]
        self.update()

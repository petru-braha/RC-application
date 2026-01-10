import flet as ft

from .members import Chat

class ChatFrame(ft.Container):
    """
    Predefined frame to encapsulate the chat history boxes.

    Displays a standard default message when no chat is active or no connection was created.
    """

    _EMPTY_LEN: int = 1
    """
    Number of layers when there are no connections.
    """

    def __init__(self) -> None:
        """
        Initialize the ChatFrame with a default welcome message.
        """
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
        """
        Selects and displays the specified chat interface.

        Args:
            chat (obj): The chat component to display.
        """
        self.content = chat
        self.update()

    def rem_chat(self, chat: Chat) -> None:
        """
        Removes the specified chat and reverts to the default layer.

        Args:
            chat (obj): The chat component to remove.
        """
        self.content = self.default_layer
        self.update()

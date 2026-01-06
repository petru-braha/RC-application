import flet as ft

from .members import Chat

class ChatFrame(ft.Stack):
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
            controls=[default_layer],
            expand=True
        )
        self.default_layer = default_layer
        self.active_layer = None

    def add_chat(self, chat: Chat) -> None:
        self.controls.append(chat)
        self.update()
        self.set_chat(chat)

    def rem_chat(self, chat: Chat) -> None:
        chat.hide()
        chat_idx = self.controls.index(chat)
        self.controls.pop(chat_idx)

        if self.active_layer != chat:
            return
        
        self.active_layer = None
        # The chat wanted for removal was active.
        # Switch to the next available layer.
        if len(self.controls) == ChatFrame._EMPTY_LEN:
            # The default layer will be visible by default.
            return
        
        # Try display the chat of a previously created connection.
        # If not possible, try to display the chat of a next connection.
        if chat_idx > ChatFrame._EMPTY_LEN:
            prev_chat = self.controls[chat_idx - 1]
            self._set_active(prev_chat)
            return
        
        if chat_idx < len(self.controls) - 1:
            next_chat = self.controls[chat_idx + 1]
            self._set_active(next_chat)
    
    def set_chat(self, chat: Chat) -> None:
        self._set_active(chat)

    def _set_active(self, chat: Chat) -> None:
        if self.active_layer:
            self.active_layer.hide()
        self.active_layer = chat
        self.active_layer.show()

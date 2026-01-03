import flet as ft

from frontend import HistoryContext, PresenceChangeable
from network import Connection

from structs import History, Dialogue

from .dialogue_list import DialogueList
    
class HistoryBox(ft.Container, PresenceChangeable):
    def __init__(self, connection: Connection, history_context: HistoryContext):
        self.connection = connection
        self.cmd_textbox = ft.TextField(
            hint_text="Type a command.",
            on_submit=connection.add_pending)

        content = ft.Column([
                DialogueList(),
                ft.Divider(),
                ft.Row([self.cmd_textbox], alignment=ft.MainAxisAlignment.CENTER)
            ],
            expand=True
        )

        super().__init__(
            content=content,
            bgcolor=ft.Colors.BLUE_GREY_800,
            padding=10,
            expand=True,
        )

        # Add self to history_context.
        history_context.controls.append(self)
        history_context.update()

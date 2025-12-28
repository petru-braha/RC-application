import flet as ft

from structs import History

from .members import DialogueBox
from ..state import FrontendState

class ChatHistory(ft.Column):
    
    def __init__(self, expand: bool):
        super().__init__(expand=expand, scroll=ft.ScrollMode.ALWAYS, auto_scroll=True)
        FrontendState.chat_history_widget = self

    def set_hist(self, hist: History):
        self.controls = [DialogueBox(d) for d in hist]
        self.update()

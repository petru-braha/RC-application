import flet as ft
from structs import Dialogue

class DialogueBox(ft.Container):
    def __init__(self, dialogue: Dialogue) -> None:
        super().__init__()
        self.content = ft.Column(
            controls=[
                ft.TextField(value=dialogue.cmd, label="Command", read_only=True),
                ft.TextField(value=str(dialogue.output), label="Output", read_only=True, multiline=True)
            ]
        )
        self.padding = 10

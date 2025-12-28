import flet as ft
from structs import History, Dialogue
from . import DialogueBox

class DialogueList(ft.Column):
    def __init__(self, expand: bool):
        super().__init__(expand=expand, scroll=ft.ScrollMode.ALWAYS, auto_scroll=True)

    def set_hist(self, hist: History):
        self.controls = [DialogueBox(d) for d in hist]
        self.update()

    def add_dialogue(self, dialogue: Dialogue):
        self.controls.append(DialogueBox(dialogue))
        self.update()

class CmdTextbox(ft.TextField):
    def __init__(self):
        super().__init__(hint_text="Type a command.", on_submit=self.on_enter)
    
    def on_enter(self, e):
        # Todo: Implement command sending logic
        pass

class HistoryBox(ft.Container):
    def __init__(self):
        self.dialogue_list = DialogueList(expand=True)
        self.cmd_textbox = CmdTextbox()

        content = ft.Column([
                self.dialogue_list,
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

    def update_history(self, hist: History):
        self.dialogue_list.set_hist(hist)

import flet as ft

from .components import ChatHistory, ChatTextbox

class RightPanel(ft.Container):
    def __init__(self):

        content = ft.Column([
                ChatHistory(),
                ft.Divider(),
                ft.Row([ChatTextbox()], alignment=ft.MainAxisAlignment.CENTER)],
            expand=True
        )

        super().__init__(
            content=content,
            bgcolor=ft.Colors.BLUE_GREY_800,
            padding=10,
            expand=True,
        )

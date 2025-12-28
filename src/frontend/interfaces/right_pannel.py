import flet as ft

class RightPanel(ft.Container):
    
    def __init__(self, content: ft.Control):
        super().__init__(
            content=content,
            bgcolor=ft.Colors.BLUE_GREY_800,
            padding=10,
            expand=True,
        )

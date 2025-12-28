import flet as ft

from frontend.interfaces import RightPanel

class DefaultRightPanel(RightPanel):

    def __init__(self):
        content=ft.Column([
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
            content=content,
        )

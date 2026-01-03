import flet as ft

class HistoryContext(ft.Stack):

    def __init__(self):
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

    def reset(self):
        self.controls = [self.default_layer]
        self.update()

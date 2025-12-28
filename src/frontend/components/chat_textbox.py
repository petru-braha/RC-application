import flet as ft

class ChatTextbox(ft.TextField):
    
    def __init__(self):
        super().__init__(hint_text="Type an command.")

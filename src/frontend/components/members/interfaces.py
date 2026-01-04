import flet as ft

class PresenceChangeable(ft.Control):
    def show(self):
        self.visible = True
        self.page.update()
    
    def hide(self):
        self.visible = False
        self.page.update()

import flet as ft

class PresenceChangeable(ft.Control):
    def show(self):
        self.visible = True
        self.page.update()
    
    def hide(self):
        self.visible = False
        self.page.update()

class ConnectionModal:
    def _update_ui(self):
        if self.open and self.page:
            self.page.update()

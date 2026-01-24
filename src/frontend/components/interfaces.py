import flet as ft

class PresenceChangeable(ft.Control):
    """
    Controls that live within a page and can show/hide themselves.
    """
    
    def show(self):
        """
        Makes the control visible and updates the page.
        """
        self.visible = True
        self.update()
    
    def hide(self):
        """
        Makes the control invisible and updates the page.
        """
        self.visible = False
        self.update()

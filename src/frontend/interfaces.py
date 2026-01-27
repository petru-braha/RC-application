import flet as ft

class ModalBase(ft.Container):
    """
    Base container style for all modal views.
    """
    
    def __init__(self):
        """
        Initialize the modal base style with standard layout properties.
        """
        super().__init__(
            bgcolor=ft.Colors.SURFACE,
            padding=20,
            border_radius=10,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK_12),
            width=450,
            height=600
        )

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

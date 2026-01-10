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

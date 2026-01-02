import flet as ft 

from .left_panel import LeftPannel
from .sidebar_default import SidebarDefault

class Layout(ft.Stack):
    def __init__(self) -> None:

        sidebar_context = ft.Stack(
            expand=True
        )

        controls: list[ft.Control] = [
            ft.Row([
                LeftPannel(sidebar_context),
                sidebar_context],
                expand=True),
                
            # todo log context 
        ]
        super().__init__(
            controls=controls,
            # The layout should cover the entire window.
            expand=True
        )

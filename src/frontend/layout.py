import flet as ft 

from .left_panel import LeftPannel
from .right_panel import RightPanel

class Layout(ft.Stack):
    def __init__(self) -> None:
        controls = [
            ft.Row([
                LeftPannel(),
                RightPanel()],
                expand=True),
                
            # todo log context 
        ]
        super().__init__(
            controls=controls,
            expand=True
        )

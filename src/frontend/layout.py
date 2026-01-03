import flet as ft 

from .left_panel import LeftPannel
from .history_context import HistoryContext

# todo consider using SafeArea 
class Layout(ft.Stack):
    def __init__(self) -> None:

        history_context = HistoryContext()

        controls: list[ft.Control] = [
            ft.Row(
                [LeftPannel(history_context), history_context],
                expand=True),
            # todo log context 
        ]
        super().__init__(
            controls=controls,
            # The layout should cover the entire window.
            expand=True
        )

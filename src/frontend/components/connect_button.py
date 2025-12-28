import flet as ft
from typing import Callable

class ConnectButton(ft.Button):

    def __init__(self, on_click: Callable) -> None:
        super().__init__("Connect", on_click=on_click)

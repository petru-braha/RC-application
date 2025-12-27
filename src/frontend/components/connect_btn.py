import flet as ft
from typing import Callable
from .popups import ConnectPopup, ManualConnectPopup    

class ConnectButton(ft.Button):

    def __init__(self, page: ft.Page, text: str = "Connect", on_click: Callable = on) -> None:

        def on_manual_connect():
            """
            Creating a second dialog object and opening it usually overlays or replaces.
            """
            popup2 = ManualConnectPopup(page, on_continue=on_manual_continue, on_back=on_manual_back)
            page.show_dialog(popup2)
            popup2.open = True
            page.update()

        def on_connect_continue(data):
                # todo parse url
                connection_list.add_connection(data)

        def on_url_connect(_=None):
            """
            Opens the url connect popup.
            """
            popup1 = ConnectPopup(page, on_continue=on_connect_continue, on_manual=on_manual_connect)
            page.show_dialog(popup1)
            popup1.open = True
            page.update()

        super().__init__(text, on_click=on_click)
        

connect_btn = ConnectButton()

import flet as ft 

from .components import Agenda, ConnectModal
from .left_panel import LeftPannel
from .components import ChatFrame

class Layout(ft.Stack):
    def __init__(self) -> None:

        agenda = Agenda()
        chat_frame = ChatFrame()
        connect_modal = ConnectModal(
            on_adenda_insert=agenda.insert,
            on_adenda_remove=agenda.remove,
            on_chat_insert=chat_frame.set_chat)
        connect_button = ft.Button("Connect", on_click=connect_modal.show)
        
        controls: list[ft.Control] = [
            ft.Row(
                [LeftPannel(agenda, connect_button), chat_frame],
                expand=True),
            # todo log context 
        ]
        super().__init__(
            controls=controls,
            # The layout should cover the entire window.
            expand=True
        )

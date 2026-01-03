import flet as ft 

from .components import Agenda, ChatFrame, ModalController
from .left_panel import LeftPannel

class Layout(ft.Stack):
    def __init__(self) -> None:

        agenda = Agenda()
        chat_frame = ChatFrame()
        modal_controller = ModalController(
            on_adenda_insert=agenda.insert,
            on_adenda_remove=agenda.remove,
            on_chat_insert=chat_frame.set_chat,
            on_chat_remove=chat_frame.reset)
        connect_button = ft.Button("Connect", on_click=modal_controller.show)
        
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

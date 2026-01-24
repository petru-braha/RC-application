import flet as ft
from typing import Callable

import core
from network import Connection

from .components import Agenda, ChatFrame, ModalController, ConnectionBox
from .left_panel import LeftPanel

logger = core.get_logger(__name__)

class Layout(ft.Stack):
    """
    Configures and arranges the main semantic sections of the application.
    """
    
    def __init__(self, add_conn_callback: Callable[[tuple], None]) -> None:
        """
        Initializes the layout controls, including Agenda, ChatFrame, and ModalController.
        """
        agenda = Agenda()
        chat_frame = ChatFrame()
        modal_controller = ModalController(add_conn_callback=add_conn_callback)
        connect_btn = ft.Button("Connect", on_click=modal_controller.show)
        
        controls = [
            ft.Row(
                [LeftPanel(agenda, connect_btn), chat_frame],
                expand=True),
            modal_controller,
        ]
        super().__init__(
            controls=controls,
            expand=True
        )
        self.agenda = agenda
        self.chat_frame = chat_frame
        self.conn_boxes_dict: dict[Connection, ConnectionBox] = {}

import flet as ft
from typing import Callable

import core
from network import Connection

from .components import Agenda, ConnBox
from .agenda_frame import AgendaFrame
from .chat_frame import ChatFrame
from .modal import Modal

logger = core.get_logger(__name__)

class Layout(ft.Stack):
    """
    Configures and arranges the main semantic sections of the application.
    """
    
    def __init__(self, add_conn_callback: Callable[[tuple], None]) -> None:
        """
        Initializes the layout controls, including Agenda, ChatFrame, and Modal.
        """
        agenda = Agenda()
        chat_frame = ChatFrame()
        modal_controller = Modal(add_conn_callback=add_conn_callback)
        connect_btn = ft.Button("Connect", on_click=modal_controller.show)
        
        controls = [
            ft.Row(
                [AgendaFrame(agenda, connect_btn), chat_frame],
                expand=True),
            modal_controller,
        ]
        super().__init__(
            controls=controls,
            expand=True
        )
        self.agenda = agenda
        self.chat_frame = chat_frame
        self.conn_boxes_dict: dict[Connection, ConnBox] = {}

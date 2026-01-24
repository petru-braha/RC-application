import flet as ft
from typing import Callable

import core
from network import Connection

from .components import ConnBox
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
        modal = Modal(add_conn_callback=add_conn_callback)
        agenda_frame = AgendaFrame(show_modal_callback=modal.show)
        chat_frame = ChatFrame()
        
        controls = [
            ft.Row(
                [agenda_frame, chat_frame],
                expand=True),
            modal,
        ]
        super().__init__(
            controls=controls,
            expand=True
        )
        self.agenda_frame = agenda_frame
        self.chat_frame = chat_frame
        self.conn_boxes_dict: dict[Connection, ConnBox] = {}

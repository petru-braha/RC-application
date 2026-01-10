import flet as ft 

from .components import Agenda, ChatFrame, ModalController
from .left_panel import LeftPanel

class Layout(ft.Stack):
    """
    Configures and arranges the main semantic sections of the application.
    """
    
    def __init__(self) -> None:
        """
        Initializes the layout controls, including Agenda, ChatFrame, and ModalController.
        """

        agenda = Agenda()
        chat_frame = ChatFrame()
        modal_controller = ModalController(
            on_agenda_add=agenda.add_box,
            on_agenda_rem=agenda.rem_box,
            on_chat_sel=chat_frame.sel_chat,
            on_chat_rem=chat_frame.rem_chat)
        connect_button = ft.Button("Connect", on_click=modal_controller.show)
        
        controls: list[ft.Control] = [
            ft.Row(
                [LeftPanel(agenda, connect_button), chat_frame],
                expand=True),
            modal_controller,
        ]
        super().__init__(
            controls=controls,
            expand=True
        )

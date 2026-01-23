import flet as ft
from typing import Callable

import core
from network import Connection
from reactor import enque_new_connection, enque_close_connection

from .components import Agenda, ChatFrame, ModalController, Chat, ConnectionBox
from .left_panel import LeftPanel

logger = core.get_logger(__name__)

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
        add_conn_callback = lambda conn_data: self.add_conn(conn_data)
        modal_controller = ModalController(add_conn_callback=add_conn_callback)
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
        self.agenda = agenda
        self.chat_frame = chat_frame

    def add_conn(self, conn_data: tuple) -> None:
        """
        Receives the connection details and creates a new Connection.
        Sets up UI components (Chat, ConnectionBox), and enqueues the connection to the reactor.

        Args:
            conn_data (arr): A tuple containing connection arguments (host, port, user, pass, db).
        """
        try:
            connection = Connection(*conn_data)
        except core.ConnectionCountError:
            logger.error(
                "Can not add a new connection.\n"
                "Remove old connections or restart the application with a new \".env\" configuration.")
            return
        
        connection_box = ConnectionBox(
            text=str(connection.addr),
            on_click=lambda: self.chat_frame.sel_chat(chat),
            on_close=lambda: self.rem_conn(connection, connection_box))
        self.agenda.add_box(connection_box)

        chat = Chat(
            text=str(connection.addr),
            on_enter=connection.sender.add_pending)
        self.chat_frame.sel_chat(chat)
        
        enque_new_connection(connection, on_response=chat.on_response)

    def rem_conn(self, conn: Connection, box: ConnectionBox) -> None:
        """
        Removes the connection, its box, and chat.

        Args:
            conn (obj): A tuple containing connection arguments (host, port, user, pass, db).
            box (obj): The connection box to be removed.
        
        Raises:
            KeyError: if the connection was not registered.
        """
        self.agenda.rem_box(box)
        self.chat_frame.rem_chat()
        
        enque_close_connection(conn)

import flet as ft

import core
from network import Connection
from reactor import ReactorClient

from .components import Agenda, ChatFrame, ModalController, Chat, ConnectionBox
from .left_panel import LeftPanel

logger = core.get_logger(__name__)

class Layout(ft.Stack):
    """
    Configures and arranges the main semantic sections of the application.
    """
    
    def __init__(self, reactor_client: ReactorClient) -> None:
        """
        Initializes the layout controls, including Agenda, ChatFrame, and ModalController.
        """
        agenda = Agenda()
        chat_frame = ChatFrame()
        add_conn_callback = lambda conn_data: self.add_conn(conn_data)
        modal_controller = ModalController(add_conn_callback=add_conn_callback)
        connect_btn = ft.Button("Connect", on_click=modal_controller.show)
        
        controls: list[ft.Control] = [
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
        self.reactor_client = reactor_client

    def add_conn(self, conn_data: tuple) -> None:
        """
        Receives the connection details and creates a new Connection.
        Sets up UI components (Chat, ConnectionBox), and enqueues the connection to the reactor.

        Args:
            conn_data (arr): A tuple containing connection arguments (host, port, user, pass, db).
        """
        try:
            # We get the connection object but it remains in read mode.
            conn = self.reactor_client.enqueue_new_conn(conn_data)
        except core.ConnectionCountError:
            logger.error(
                "Can not add a new connection.\n"
                "Remove old connections or restart the application with a new \".env\" configuration.")
            return
        
        conn_host = conn_data[0]
        chat = Chat(
            text=conn_host,
            on_enter=lambda cmd: self.reactor_client.enqueue_cmd(conn, cmd))
        self.chat_frame.sel_chat(chat)
        self.reactor_client.bind_chat(conn, chat)
        
        connection_box = ConnectionBox(
            text=conn_host,
            on_click=lambda: self.chat_frame.sel_chat(chat),
            on_close=lambda: self.rem_conn(conn, connection_box))
        self.agenda.add_box(connection_box)

    def rem_conn(self, conn: Connection, box: ConnectionBox) -> None:
        """
        Removes the connection, its box, and chat.

        Args:
            conn (obj): A tuple containing connection arguments (host, port, user, pass, db).
            box (obj): The connection box to be removed.
        
        Raises:
            KeyError: if the connection was not registered.
        """
        self.reactor_client.enqueue_close_conn(conn)
        self.agenda.rem_box(box)
        self.chat_frame.rem_chat()

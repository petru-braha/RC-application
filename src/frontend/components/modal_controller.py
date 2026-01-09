import flet as ft
from typing import Callable

from core.config import get_logger
from core.exceptions import ConnectionCountError
from network import Connection

from reactor import enque_new_connection, enque_close_connection

from .members import Chat, ConnectionBox, PresenceChangeable
from .modals import ManualConnect, UrlConnect

logger = get_logger(__name__)

class _ControllerBase:
    """
    Base class for modal controller that handle the creation and deletion of connections.
    """

    def __init__(self,
                 on_agenda_add: Callable,
                 on_agenda_rem: Callable,
                 on_chat_sel: Callable,
                 on_chat_rem: Callable):
        """
        Initializes the controller with callbacks for managing UI components.

        Args:
            on_agenda_add (lambda): Callback to add an item to the agenda.
            on_agenda_rem (lambda): Callback to remove an item from the agenda.
            on_chat_sel (lambda): Callback to select a chat.
            on_chat_rem (lambda): Callback to remove a chat.
        """
        self._on_agenda_add = on_agenda_add
        self._on_agenda_rem = on_agenda_rem
        self._on_chat_sel = on_chat_sel
        self._on_chat_rem = on_chat_rem

    def on_continue(self, connection_data: tuple) -> None:
        """
        Handles the continuation process after connection details are provided.
        Creates a new Connection, sets up UI components (Chat, ConnectionBox),
        and enqueues the connection to the reactor.

        Args:
            connection_data (arr): A tuple containing connection arguments (host, port, user, pass, db).
        """
        try:
            connection = Connection(*connection_data)
        except ConnectionCountError:
            logger.error(
                "Can not add a new connection.\n"
                "Remove old connections or restart the application with a new \".env\" configuration.")
            return
        
        chat = Chat(
            text=str(connection.addr),
            on_enter=connection.sender.add_pending)
        self._on_chat_sel(chat)

        def on_connection_close():
            enque_close_connection(connection)
            self._on_chat_rem(chat)
        connection_box = ConnectionBox(
            text=str(connection.addr),
            on_click=lambda: self._on_chat_sel(chat),
            on_connection_close=on_connection_close,
            on_agenda_rem=self._on_agenda_rem)
        self._on_agenda_add(connection_box)
        
        enque_new_connection(connection, on_response=chat.on_response)
        self.hide()

class ModalController(ft.Container, _ControllerBase, PresenceChangeable):
    """
    Handles the creation and the deletion of connections through the reactor.
    Manages switching between Manual and URL connection modes.
    ACTS as an overlay container (modal).
    """

    def __init__(self,
                 on_agenda_add: Callable,
                 on_agenda_rem: Callable,
                 on_chat_sel: Callable,
                 on_chat_rem: Callable):
        """
        Initializes the modal controller with views for manual and URL connection modes.

        Args:
             on_agenda_add (lambda): Callback to add an item to the agenda.
             on_agenda_rem (lambda): Callback to remove an item from the agenda.
             on_chat_sel (lambda): Callback to select a chat.
             on_chat_rem (lambda): Callback to remove a chat.
        """
        ControllerBase.__init__(
            self,
            on_agenda_add,
            on_agenda_rem,
            on_chat_sel,
            on_chat_rem
        )

        close_btn = ft.IconButton(ft.Icons.CLOSE, on_click=self.hide, tooltip="Close")
        self.url_view = UrlConnect(
            on_continue=self.on_continue,
            switch_btn=ft.Button("Switch to manual mode", on_click=self.switch_modal),
            close_btn=close_btn
        )
        self.manual_view = ManualConnect(
            on_continue=self.on_continue,
            switch_btn=ft.Button("Switch to URL mode", on_click=self.switch_modal),
            close_btn=close_btn
        )
        
        ft.Container.__init__(
            self,
            content=self.url_view,
            expand=True,
            bgcolor=ft.Colors.BLACK_54,
            alignment=ft.Alignment.CENTER,
            visible=False
        )
        self.is_manual = False
    
    def switch_modal(self, event):
        """
        Switches between manual and URL connection views.
        
        Args:
            event (obj): The event object.
        """
        if self.is_manual:
            self.content = self.url_view
        else:
            self.content = self.manual_view
        self.is_manual = not self.is_manual
        self.page.update()

import flet as ft
from typing import Callable

from core import Operator
from frontend import PresenceChangeable
from .modals import ManualConnect, UrlConnect

from network import Connection

from .members import Chat, ConnectionBox

class ControllerBase:
    """
    Base class for modal controller that handle the creation and deletion of connections.
    """

    def __init__(self,
                 on_agenda_insert: Callable,
                 on_agenda_remove: Callable,
                 on_chat_insert: Callable,
                 on_chat_remove: Callable):
        self._on_agenda_insert = on_agenda_insert
        self._on_agenda_remove = on_agenda_remove
        self._on_chat_insert = on_chat_insert
        self._on_chat_remove = on_chat_remove

    def on_continue(self, connection_data: tuple) -> None:
        connection = Connection(connection_data)
        
        chat = Chat(on_enter=connection.add_pending)
        self._on_chat_insert(chat)

        def on_connection_close():
            Operator.remove_connection(connection)
            self._on_chat_remove(chat)
        connection_box = ConnectionBox(
            connection.addr,
            on_click=chat.show,
            on_close=on_connection_close,
            on_agenda_remove=self._on_agenda_remove)
        self._on_agenda_insert(connection_box)
        
        Operator.register_connection(connection, on_response=chat.on_response)
        self.hide()

class ModalController(ft.Container, ControllerBase, PresenceChangeable):
    """
    Handles the creation and the deletion of connections through the reactor.
    Manages switching between Manual and URL connection modes.
    ACTS as an overlay container (modal).
    """

    def __init__(self,
                 on_agenda_insert: Callable,
                 on_agenda_remove: Callable,
                 on_chat_insert: Callable,
                 on_chat_remove: Callable):
        ControllerBase.__init__(
            self,
            on_agenda_insert,
            on_agenda_remove,
            on_chat_insert,
            on_chat_remove)

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
            alignment=ft.Alignment.CENTER)
        self.visible = False
        self.is_manual = False
    
    def switch_modal(self, e):
        if self.is_manual:
            self.content = self.url_view
            self.is_manual = False
        else:
            self.content = self.manual_view
            self.is_manual = True
        self.page.update(e)

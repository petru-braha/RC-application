import flet as ft
from typing import Callable

from core import Operator
from network import Connection

from .components import Chat, ConnectionBox

class PresenceChangeable(ft.Control):
    def show(self):
        self.visible = True
        self.page.update()
    
    def hide(self):
        self.visible = False
        self.page.update()

class ConnectionModal(PresenceChangeable, ft.AlertDialog):
    def __init__(self, on_agenda_insert: Callable, on_agenda_remove: Callable, on_chat_insert: Callable, on_chat_remove: Callable):
        ft.AlertDialog.__init__()
        self._on_agenda_insert = on_agenda_insert
        self._on_agenda_remove = on_agenda_remove
        self._on_chat_insert = on_chat_insert
        self._on_chat_remove = on_chat_remove

    def on_continue(self, connection_data: tuple) -> None:
        connection = Connection(connection_data)
        
        chat = Chat(on_enter=connection.add_pending)
        self._on_chat_insert(chat)

        def on_connection_close(self):
            Operator.remove_connection(connection)
            self._on_chat_remove(chat)
        connection_box = ConnectionBox(
            connection.addr,
            on_click=chat.show,
            on_close=on_connection_close,
            on_adenga_remove=self._on_agenda_remove)
        self._on_agenda_insert(connection_box)
        
        Operator.register_connection(connection, on_response=chat.on_response)
        self.hide()

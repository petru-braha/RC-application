import flet as ft
from typing import Callable

from .components import PresenceChangeable
from .modals import ManualConnect, UrlConnect

class ModalController(ft.Container, PresenceChangeable):
    """
    Handles the creation and the deletion of connections through the reactor.
    Manages switching between Manual and URL connection modes.
    ACTS as an overlay container (modal).
    """

    def __init__(self, add_conn_callback: Callable[[tuple], None]) -> None:
        """
        Initializes the modal controller with views for manual and URL connection modes.

        Args:
            add_conn_callback (lambda): To be called when user enters connection data and **continues**.
        """        
        close_btn = ft.IconButton(ft.Icons.CLOSE, on_click=self.hide, tooltip="Close")
        url_view = UrlConnect(
            on_continue=self.on_continue,
            switch_btn=ft.Button("Switch to manual mode", on_click=self.switch_modal),
            close_btn=close_btn
        )
        manual_view = ManualConnect(
            on_continue=self.on_continue,
            switch_btn=ft.Button("Switch to URL mode", on_click=self.switch_modal),
            close_btn=close_btn
        )
        
        ft.Container.__init__(
            self,
            content=url_view,
            expand=True,
            bgcolor=ft.Colors.BLACK_54,
            alignment=ft.Alignment.CENTER,
            visible=False
        )
        self._add_conn_callback = add_conn_callback
        self._is_manual = False
        self._url_view = url_view
        self._manual_view = manual_view

    def on_continue(self, conn_data: tuple) -> None:
        """
        Forwards the connection data and closes the modal.

        Args:
            conn_data (arr): Data to instantiate the connection object.
        """
        self._add_conn_callback(conn_data)
        self.hide()
    
    def switch_modal(self, event) -> None:
        """
        Switches between manual and URL connection views.
        
        Args:
            event (obj): The event object.
        """
        if self._is_manual:
            self.content = self._url_view
        else:
            self.content = self._manual_view
        self._is_manual = not self._is_manual
        self.update()

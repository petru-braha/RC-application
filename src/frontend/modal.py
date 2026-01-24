import flet as ft
from typing import Callable

from .interfaces import PresenceChangeable
from .modal_views import ManualView, UrlView

class Modal(ft.Container, PresenceChangeable):
    """
    Though text field(s) takes connection creation details and forwards them to the reactor.
    - url view - only one text field for the url
    - manual view - the user has to insert the host, port, and other data
    """

    def __init__(self, add_conn_callback: Callable[[tuple], None]) -> None:
        close_btn = ft.IconButton(ft.Icons.CLOSE, on_click=self.hide, tooltip="Close")
        url_view = UrlView(
            on_continue=self.on_continue,
            switch_btn=ft.Button("Switch to manual mode", on_click=self.switch_view),
            close_btn=close_btn
        )
        manual_view = ManualView(
            on_continue=self.on_continue,
            switch_btn=ft.Button("Switch to URL mode", on_click=self.switch_view),
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
        self.url_view = url_view
        self.manual_view = manual_view
        self._add_conn_callback = add_conn_callback
        self._is_manual = False

    def on_continue(self, conn_data: tuple) -> None:
        """
        Forwards the connection data and closes the modal.

        Args:
            conn_data (arr): Data to instantiate the connection object.
        """
        self._add_conn_callback(conn_data)
        self.hide()
    
    def switch_view(self, event) -> None:
        """
        Switches between manual and url connection views.
        
        Args:
            event (obj): The event object.
        """
        if self._is_manual:
            self.content = self.url_view
        else:
            self.content = self.manual_view
        self._is_manual = not self._is_manual
        self.update()

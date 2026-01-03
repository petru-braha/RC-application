import flet as ft
from typing import Callable

from frontend import PresenceChangeable, ConnectionBase
from .modals import ManualConnect, UrlConnect

class ModalController(ConnectionBase, PresenceChangeable, ft.Container):
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
        ConnectionBase.__init__(self, on_agenda_insert, on_agenda_remove, on_chat_insert, on_chat_remove)
        ft.Container.__init__(self)
        
        self.manual_view = ManualConnect(on_continue=self.on_continue)
        self.url_view = UrlConnect(on_continue=self.on_continue)
        
        self.current_view = self.manual_view
        self.is_manual = True

        self.switch_btn = ft.Button("Switch to URL Mode", on_click=self.switch_modal)
        self.close_btn = ft.IconButton(ft.Icons.CLOSE, on_click=self.hide, tooltip="Close")

        # Container styling for Modal Overlay
        self.visible = False # Hidden by default
        self.alignment = ft.alignment.center
        self.bgcolor = ft.colors.BLACK54
        self.expand = True
        self.on_click = lambda e: None
        
        self.dialog_content = ft.Container(
            bgcolor=ft.colors.SURFACE,
            padding=20,
            border_radius=10,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.colors.BLACK12),
            width=450,
            height=600,
        )
        self.content = self.dialog_content
        
        self.update_content()


    def switch_modal(self, e):
        if self.is_manual:
            self.current_view = self.url_view
            self.switch_btn.text = "Switch to Manual Mode"
            self.is_manual = False
        else:
            self.current_view = self.manual_view
            self.switch_btn.text = "Switch to URL Mode"
            self.is_manual = True
        
        self.update_content()
        self.page.update()

    def update_content(self):
        header = ft.Row([ft.Container(expand=True), self.close_btn], alignment=ft.MainAxisAlignment.END)
        
        inner_content = ft.Column(
            [
                header,
                self.current_view,
                ft.Divider(),
                ft.Row([self.switch_btn], alignment=ft.MainAxisAlignment.CENTER)
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True # Use available space in dialog_content
        )
        self.dialog_content.content = inner_content

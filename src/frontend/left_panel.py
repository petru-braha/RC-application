import flet as ft

from .components import ConnectButton, ConnectModal, ConnectionList
from .history_context import HistoryContext

class LeftPannel(ft.Container):
    def __init__(self, history_context: HistoryContext):
        connection_list = ConnectionList(history_context)
        connect_modal = ConnectModal(on_insert=connection_list.insert_connection)
        connect_button = ConnectButton(on_click=connect_modal.show)
        
        content = ft.Column([
            connection_list,
            ft.Divider(),
            ft.Row([connect_button], alignment=ft.MainAxisAlignment.CENTER),
        ], expand=True)

        super().__init__(
            content=content,
            width=250,
            bgcolor=ft.Colors.BLUE_GREY_900,
            padding=10,
        )

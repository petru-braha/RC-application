import flet as ft

from .components import ConnectButton, Modal, ConnectionList

class LeftPannel(ft.Container):
    def __init__(self, sidebar_context: ft.Stack):
        connection_list = ConnectionList(sidebar_context)
        modal = Modal(on_insert=connection_list.insert_connection)
        connect_button = ConnectButton(on_click=modal.open_dialog)
        
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

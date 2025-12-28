import flet as ft

from .components import ConnectButton, Modal, ConnectionList

class LeftPannel(ft.Container):
    def __init__(self):
        connection_list = ConnectionList()
        modal = Modal(on_insert=connection_list.insert_connection)
        connect_btn = ConnectButton(on_click=modal.open_dialog)
        
        content = ft.Column([
            connection_list,
            ft.Divider(),
            ft.Row([connect_btn], alignment=ft.MainAxisAlignment.CENTER),
        ], expand=True)

        super().__init__(
            content=content,
            width=250,
            bgcolor=ft.Colors.BLUE_GREY_900,
            padding=10,
        )

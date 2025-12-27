import flet as ft
from frontend.components.connection_list import ConnectionList
from frontend.components.chat_view import ChatView
from frontend.components.popups import ConnectPopup, ManualConnectPopup

from frontend.connection_box import ConnectionBox
from frontend.log_box import LogBox

def main(page: ft.Page):
    page.title = "RC-application"
    page.theme_mode = ft.ThemeMode.DARK
    chat_view = ChatView()

    def on_connection_select(conn_info):
        chat_view.set_connection(conn_info)

    def on_url_connect(_=None):
        """
        Opens the url connect popup.
        """
        popup1 = ConnectPopup(page, on_continue=on_connect_continue, on_manual=on_manual_connect)
        page.show_dialog(popup1)
        popup1.open = True
        page.update()

    def on_connect_continue(data):
        # todo parse url
        connection_list.add_connection(data)

    def on_manual_connect():
        popup2 = ManualConnectPopup(page, on_continue=on_manual_continue, on_back=on_manual_back)
        page.show_dialog(popup2)
        popup2.open = True
        page.update()

    def on_manual_continue(data):
        connection_list.add_connection(data)
        
    def on_manual_back():
        # Callback from Popup 2 Back button
        # Re-open Popup 1
        on_url_connect()
    
    # Layout
    static_connect_btn = ft.Button("Connect", on_click=on_url_connect)
    connection_list = ConnectionList(on_select=on_connection_select)

    static_textbox = ft.TextField(hint_text="Type an command.")
    
    left_panel = ft.Container(
        width=250,
        bgcolor=ft.Colors.BLUE_GREY_900,
        padding=10,
        content=ft.Column([
            connection_list,
            ft.Divider(),
            ft.Row([static_connect_btn], alignment=ft.MainAxisAlignment.CENTER),
        ], expand=True)
    )

    right_panel = ft.Container(
        expand=True,
        bgcolor=ft.Colors.BLUE_GREY_800,
        padding=10,
        content=ft.Column([
            chat_view,
            ft.Divider(),
            ft.Row([static_textbox], alignment=ft.MainAxisAlignment.CENTER),
        ], expand=True)
    )

    layout = ft.Stack([
        ft.Row(
            [
                left_panel,
                right_panel
            ],
            expand=True
        ),
    ], expand=True)

    page.add(layout)
    layout.controls.append(ft.Column([LogBox("lmao")], alignment=ft.MainAxisAlignment.START))

ft.run(main)

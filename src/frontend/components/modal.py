import flet as ft
from typing import Callable

from network import Connection, UrlConnection

class Modal(ft.AlertDialog):
    def __init__(self, on_insert: Callable):
        super().__init__()
        self.on_insert = on_insert
        
        # Internal State Fields
        self.url_input = ft.TextField(
            hint_text="redis://user:pass@host:port/db", 
            text_align=ft.TextAlign.CENTER
        )
        
        self.host_input = ft.TextField(hint_text="Host")
        self.port_input = ft.TextField(hint_text="Port")
        self.user_input = ft.TextField(hint_text="Username")
        self.pass_input = ft.TextField(
            hint_text="Password", 
            password=True, 
            can_reveal_password=True
        )
        self.db_input = ft.TextField(hint_text="Database Index")

        # Initialize with URL mode
        self.set_url_mode()

    def set_url_mode(self):
        close_btn = ft.IconButton(ft.Icons.CLOSE, on_click=self.close_dialog, tooltip="Close")
        manual_btn = ft.Button("Manual connection info", on_click=lambda e: self.set_manual_mode())
        continue_btn = ft.Button("Continue", on_click=self.on_url_continue)
        prompt = ft.Text("Paste the connection url", text_align=ft.TextAlign.CENTER)

        header = ft.Row([ft.Container(expand=True), close_btn], alignment=ft.MainAxisAlignment.END)

        self.content = ft.Container(
            width=400,
            height=300,
            content=ft.Column(
                [
                    header,
                    ft.Container(height=20), # Spacer
                    ft.Row([manual_btn], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([prompt], alignment=ft.MainAxisAlignment.CENTER),
                    self.url_input,
                    ft.Row([continue_btn], alignment=ft.MainAxisAlignment.CENTER),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        self._update_ui()

    def set_manual_mode(self):
        close_btn = ft.IconButton(ft.Icons.CLOSE, on_click=self.close_dialog, tooltip="Close")
        back_btn = ft.Button("Back", on_click=lambda e: self.set_url_mode())
        continue_btn = ft.Button("Continue", on_click=self.on_manual_continue)
        prompt = ft.Text("Paste manual connection info", text_align=ft.TextAlign.CENTER)

        header = ft.Row([ft.Container(expand=True), close_btn], alignment=ft.MainAxisAlignment.END)

        self.content = ft.Container(
            width=400,
            height=500,
            content=ft.Column(
                [
                    header,
                    ft.Row([back_btn], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([prompt], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.host_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.port_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.user_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.pass_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.db_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=10),
                    ft.Row([continue_btn], alignment=ft.MainAxisAlignment.CENTER),
                ],
                scroll=ft.ScrollMode.AUTO
            )
        )
        self._update_ui()

    def _update_ui(self):
        if self.open and self.page:
            self.page.update()
    
    def open_dialog(self, e):
        self.open = True
        self.page.update()

    def close_dialog(self, e):
        self.open = False
        self.page.update()

    def on_url_continue(self, e):
        try:
            val = self.url_input.value
            conn = UrlConnection(val)
            self.on_insert(conn)
            self.close_dialog(e)
        except Exception as e:
            print(f"Error creating URL connection: {e}")

    def on_manual_continue(self, e):
        try:
            conn = Connection(
                host=self.host_input.value,
                port=self.port_input.value,
                user=self.user_input.value,
                pasw=self.pass_input.value,
                db_idx=self.db_input.value
            )
            self.on_insert(conn)
            self.close_dialog(e)

        except Exception as e:
            print(f"Error creating connection: {e}")

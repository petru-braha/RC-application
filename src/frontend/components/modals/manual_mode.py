import flet as ft
from typing import Callable

from core import Operator

class ManualMode(ft.AlertDialog):
    def __init__(self, on_insert: Callable):
        ft.AlertDialog.__init__(self)
        self.on_insert = on_insert
        
        self.host_input = ft.TextField(hint_text="Host")
        self.port_input = ft.TextField(hint_text="Port")
        self.user_input = ft.TextField(hint_text="Username")
        self.pass_input = ft.TextField(
            hint_text="Password", 
            password=True, 
            can_reveal_password=True
        )
        self.db_input = ft.TextField(hint_text="Database Index")
    
    def set_manual_mode(self):
        close_btn = ft.IconButton(ft.Icons.CLOSE, on_click=self.hide, tooltip="Close")
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
        if self.visible:
            self.update()

    def on_manual_continue(self, e):
        try:
            conn = Operator.add_connection(
                host=self.host_input.value,
                port=self.port_input.value,
                user=self.user_input.value,
                pasw=self.pass_input.value,
                db_idx=self.db_input.value
            )
            self.on_insert(conn)
            self.hide(e)

        except Exception as e:
            print(f"Error creating connection: {e}")

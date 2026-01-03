import flet as ft
from typing import Callable

class ManualConnect(ft.Container):
    def __init__(self, on_continue: Callable):
        super().__init__()
        
        self.host_input = ft.TextField(hint_text="Host")
        self.port_input = ft.TextField(hint_text="Port")
        self.user_input = ft.TextField(hint_text="Username")
        self.pass_input = ft.TextField(
            hint_text="Password", 
            password=True, 
            can_reveal_password=True
        )
        self.db_input = ft.TextField(hint_text="Database Index (0-15)")
    
        prompt = ft.Text("Paste manual connection info", text_align=ft.TextAlign.CENTER)
        
        continue_btn = ft.Button("Continue", on_click=self.on_process_manual)
        self._on_continue_callback = on_continue

        self.content = ft.Column(
            [
                ft.Row([prompt], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.host_input], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.port_input], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.user_input], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.pass_input], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.db_input], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=10),
                ft.Row([continue_btn], alignment=ft.MainAxisAlignment.CENTER),
            ],
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.width = 400
        self.height = 500

    def on_process_manual(self, e) -> None:
        host = self.host_input.value
        port = self.port_input.value
        user = self.user_input.value
        passw = self.pass_input.value
        db_raw = self.db_input.value
        
        try:
            db_idx = int(db_raw) if db_raw else ""
        except ValueError:
            # Handle error or default
            db_idx = ""

        # Tuple matching process_redis_url return structure
        connection_data = (host, port, user, passw, db_idx)
        self._on_continue_callback(connection_data)

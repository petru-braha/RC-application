import flet as ft

class ConnectPopup(ft.AlertDialog):
    def __init__(self, page: ft.Page, on_continue, on_manual):
        super().__init__()
        self.on_continue_callback = on_continue
        self.on_manual_callback = on_manual
        self.modal = True
        
        self.url_input = ft.TextField(hint_text="redis://user:pass@host:port/db", text_align=ft.TextAlign.CENTER)
        
        # Close button (upper right)
        # To achieve "Upper Right" in a dialog content, we might need a Column/Row structure.
        # Flet AlertDialog has 'actions' usually at bottom, or 'content' which is the body.
        # To strictly follow "upper right", we can make the content a Column.
        
        # Layout:
        # [Manual Button (Centered above prompt)]
        # [Prompt]
        # [Textbox]
        # [Continue Button]
        
        # Close button is usually handled by `actions` or a specific icon in content.
        # User said: "one button is in upper right part of the popup responsible for closing the popup."
        
        close_btn = ft.IconButton(ft.Icons.CLOSE, on_click=self.close_dialog, tooltip="Close")
        manual_btn = ft.Button("Manual connection info", on_click=self.on_manual_click)
        prompt = ft.Text("Paste the connection url", text_align=ft.TextAlign.CENTER)
        continue_btn = ft.Button("Continue", on_click=self.on_continue_click)

        # Header with Close button aligned right
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

    def close_dialog(self, e):
        self.open = False
        self.page.update()

    def on_manual_click(self, e):
        self.close_dialog(e)
        self.on_manual_callback()

    def on_continue_click(self, e):
        val = self.url_input.value
        self.close_dialog(e)
        self.on_continue_callback({"type": "url", "url": val})

class ManualConnectPopup(ft.AlertDialog):
    def __init__(self, page: ft.Page, on_continue, on_back):
        super().__init__()
        self.on_continue_callback = on_continue
        self.on_back_callback = on_back
        self.modal = True
        
        # Fields
        self.host_input = ft.TextField(hint_text="Host")
        self.port_input = ft.TextField(hint_text="Port")
        self.user_input = ft.TextField(hint_text="Username")
        self.pass_input = ft.TextField(hint_text="Password", password=True, can_reveal_password=True)
        self.db_input = ft.TextField(hint_text="Database Index")

        # Buttons
        close_btn = ft.IconButton(ft.Icons.CLOSE, on_click=self.close_dialog, tooltip="Close")
        back_btn = ft.Button("Back", on_click=self.on_back_click)
        continue_btn = ft.Button("Continue", on_click=self.on_continue_click)
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

    def close_dialog(self, e):
        self.open = False
        self.page.update()

    def on_back_click(self, e):
        self.close_dialog(e)
        self.on_back_callback()

    def on_continue_click(self, e):
        data = {
            "type": "manual",
            "host": self.host_input.value,
            "port": self.port_input.value,
            "user": self.user_input.value,
            "pass": self.pass_input.value,
            "db": self.db_input.value
        }
        self.close_dialog(e)
        self.on_continue_callback(data)

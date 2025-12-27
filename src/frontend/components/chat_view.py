import flet as ft

class ChatView(ft.Column):
    def __init__(self):
        super().__init__(expand=True)
        self.current_connection = None
        self.chat_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=10,
            auto_scroll=True
        )
        self.title_text = ft.Text("Select a connection", size=20, weight=ft.FontWeight.BOLD)
        
        self.controls = [
            ft.Container(content=self.title_text, padding=10),
            ft.Divider(height=1),
            self.chat_list
        ]

    def set_connection(self, conn_info: dict):
        self.current_connection = conn_info
        host = conn_info.get('host', 'unknown')
        port = conn_info.get('port', '')
        self.title_text.value = f"Chat with {host}:{port}"
        
        # Clear previous chat
        self.chat_list.controls.clear()
        
        # "instead of the chat history, for now, print again the host and port of that connection to the right section."
        self.chat_list.controls.append(
            ft.Text(f"Connected to {host}:{port}", italic=True)
        )
        self.update()

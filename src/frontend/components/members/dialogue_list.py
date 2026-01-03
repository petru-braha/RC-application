import flet as ft

class DialogueList(ft.ListView):
    def __init__(self) -> None:
        super().__init__(
            expand=True,
            auto_scroll=True,
            scroll=ft.ScrollMode.ALWAYS,
        )

    def add_request(self, req: str) -> None:
        # sanitizer
        # connection.append
        to_display = ft.Text(req)
        self.controls.append(to_display)
        # print text of pending

    def add_response(self, res: str) -> None:
        to_display = ft.Text(req)
        self.controls.append(to_display)

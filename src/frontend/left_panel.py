import flet as ft

from .components import Agenda

class LeftPanel(ft.Container):
    """
    Groups the agenda and the connect button under a unitary panel.
    """

    def __init__(self, agenda: Agenda, connect_btn: ft.Button) -> None:
        content = ft.Column([
            agenda,
            ft.Divider(),
            ft.Row([connect_btn], alignment=ft.MainAxisAlignment.CENTER),
        ], expand=True)

        super().__init__(
            content=content,
            width=350,
            bgcolor=ft.Colors.BLUE_GREY_900,
            padding=10,
        )

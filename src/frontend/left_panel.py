import flet as ft

from .components import Agenda

class LeftPannel(ft.Container):
    """
    Groups the agenda and the connect button under a unitary panel.
    """

    def __init__(self, agenda: Agenda, connect_button: ft.Button) -> None:
        content = ft.Column([
            agenda,
            ft.Divider(),
            ft.Row([connect_button], alignment=ft.MainAxisAlignment.CENTER),
        ], expand=True)

        super().__init__(
            content=content,
            width=250,
            bgcolor=ft.Colors.BLUE_GREY_900,
            padding=10,
        )

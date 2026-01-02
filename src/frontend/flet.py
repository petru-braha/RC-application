import flet as ft
import time as tm

from core import Config, Operator
from .layout import Layout

def build_page(page: ft.Page) -> None:
    page.title = "RC-application"
    page.theme_mode = ft.ThemeMode.DARK
    # page.add(Layout())
    
    container = ft.Container(
        content=ft.Column([
            ft.Divider(),
            # ft.Row([connect_button], alignment=ft.MainAxisAlignment.CENTER),
            ],
            expand=True),
        width=250,
        bgcolor=ft.Colors.YELLOW_200,
        padding=10
    )

    stack = ft.Stack(
        controls=[
            ft.Container(
                bgcolor=ft.Colors.RED_100,
                expand=True
            )
        ],
        expand=True,
    )

    layout = ft.Row(
        controls=[container, stack],
        expand=True
    )

    page.add(layout)
    page.update()
    color0 = ft.Colors.GREEN_100
    color1 = ft.Colors.BLUE_500
    who: bool = True

    while True:
        tm.sleep(1)
        color = color0 if who else color1
        who = not who
        
        stack.controls[0] = ft.Container(
            bgcolor=color,
            expand=True
        )
        page.update()
        return

def open_window(config: Config, operator: Operator) -> None:
    ft.run(build_page)

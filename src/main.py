import flet as ft

from frontend import Layout

from .app_reactor import AppReactor

def main(page: ft.Page):
    page.title = "RC-application"
    page.theme_mode = ft.ThemeMode.DARK
    # page.badge
    page.add(Layout())

ft.run(main)
AppReactor.close()

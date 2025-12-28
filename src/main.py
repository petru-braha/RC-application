import flet as ft

from frontend import Layout

from core.reactor import Reactor

def main(page: ft.Page):

    page.title = "RC-application"
    page.theme_mode = ft.ThemeMode.DARK
    # page.badge
    page.add(Layout())

Reactor.open()
ft.run(main)
Reactor.close()

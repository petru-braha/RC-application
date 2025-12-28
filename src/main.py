import flet as ft

from core import SelectorHolder, Reactor
from frontend import Layout

def main(page: ft.Page):

    page.title = "RC-application"
    page.theme_mode = ft.ThemeMode.DARK
    # page.badge
    page.add(Layout())

SelectorHolder.open()
Reactor.start()
ft.run(main)
SelectorHolder.close()

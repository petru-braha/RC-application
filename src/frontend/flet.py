import flet as ft

from core import Config
from .layout import Layout

def build_page(page: ft.Page) -> None:
    page.title = "RC-application"
    page.theme_mode = ft.ThemeMode.DARK
    page.add(Layout())

def open_window(config: Config) -> None:
    ft.run(build_page, assets_dir="src/frontend/assets")

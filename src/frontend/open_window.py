import flet as ft

from .layout import Layout

def build_page(page: ft.Page) -> None:
    # Handles OS intrusions gracefully.
    # Similar to a regular container.
    safe_area = ft.SafeArea(
        content=Layout(),
        expand=True
    )

    page.title = "RC-application"
    page.theme_mode = ft.ThemeMode.DARK
    page.add(safe_area)

def open_window() -> None:
    ft.run(build_page, assets_dir="src/ui/assets")

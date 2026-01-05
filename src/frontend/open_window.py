import flet as ft

from core import get_logger

from .layout import Layout

logger = get_logger(__name__)

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
    logger.info("Initializing Flet app window...")
    ft.run(build_page, assets_dir="src/frontend/assets")
    logger.info("Flet app window initialized.")

import flet as ft
from threading import Event

import core
from frontend import Layout

from multiplexing import loop_multiplexing
from util import uninterruptible

logger = core.get_logger(__name__)

@uninterruptible
async def close_page(multiplexing_event: Event, page: ft.Page) -> None:
    logger.info("Closing application...")
    try:
        multiplexing_event.clear()
    except BaseException as e:
        logger.error(f"Application failed: {e}.", exc_info=True)
    finally:
        page.window.prevent_close = False
        page.window.on_event = None
        await page.window.destroy()
        await page.window.close()

@uninterruptible
def build_page(page: ft.Page) -> None:
    try:
        multiplexing_event = Event()
        multiplexing_event.set()
        
        # Run the multiplexing loop in a background thread managed by Flet.
        page.run_thread(loop_multiplexing, multiplexing_event)
        logger.info("Multiplexing thread started.")
        
        async def handle_close(event: ft.WindowEvent | None = None) -> None:
            if event and event.data != "close" and event.type != ft.WindowEventType.CLOSE:
                return
            await close_page(multiplexing_event, page)
        
        page.window.on_event = handle_close
        page.window.prevent_close = True
        page.theme_mode = ft.ThemeMode.DARK
        page.title = "RC-application"

        # Handles OS intrusions gracefully.
        # Similar to a regular container.
        safe_area = ft.SafeArea(Layout(), expand=True)
        page.add(safe_area)
        logger.info("Flet app window initialized.")
    
    except Exception as e:
        logger.error(f"Application failed: {e}.", exc_info=True)
        page.window.close()

if __name__ == "__main__":
    if core.IS_CLI:
        raise NotImplementedError("CLI mode is not implemented yet")
        logger.info("CLI mode enabled.")
    else:
        logger.info("GUI mode enabled.")
        ft.run(build_page, assets_dir="src/frontend/assets")

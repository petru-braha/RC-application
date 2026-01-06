import flet as ft
from threading import Thread, Event

from core import IS_CLI, get_logger
from frontend import Layout

from multiplexing import run_multiplexing_loop

logger = get_logger(__name__)

def build_page(page: ft.Page) -> None:
    try:
        # Start a thread for the I/O multiplexing loop.
        multiplexing_event = Event()
        multiplexing_thread = Thread(target=run_multiplexing_loop, args=[multiplexing_event])
        multiplexing_event.set()
        multiplexing_thread.start()
        logger.info("Multiplexing thread started.")

        async def close_application(event: ft.WindowEvent | None = None) -> None:
            if event and event.data != "close" and event.type != ft.WindowEventType.CLOSE:
                return
            
            logger.info("Closing application...")
            try:
                multiplexing_event.clear()
                multiplexing_thread.join()
            except BaseException as e:
                logger.error(f"Application failed: {e}.", exc_info=True)
            finally:
                page.window.prevent_close = False
                page.window.on_event = None
                await page.window.destroy()
                await page.window.close()
        
        page.window.on_event = close_application
        page.window.prevent_close = True
        page.title = "RC-application"
        page.theme_mode = ft.ThemeMode.DARK

        # Handles OS intrusions gracefully.
        # Similar to a regular container.
        safe_area = ft.SafeArea(Layout(), expand=True)
        page.add(safe_area)
        logger.info("Flet app window initialized.")
    
    except Exception as e:
        logger.error(f"Application failed: {e}.", exc_info=True)
        close_application()
    except BaseException as e:
        logger.error(f"Application forcely closed: {e}.", exc_info=True)
        close_application()

if __name__ == "__main__":
    if IS_CLI:
        raise NotImplementedError("CLI mode is not implemented yet")
        logger.info("CLI mode enabled.")
    else:
        logger.info("GUI mode enabled.")
        ft.run(build_page, assets_dir="src/frontend/assets")

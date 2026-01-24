import flet as ft
from threading import Event

import core
from frontend import Layout

from reactor import Reactor, ReactorClient
from multiplexing import loop_multiplexing
from util import close_page, add_conn


logger = core.get_logger(__name__)

@core.uninterruptible
def build_page(page: ft.Page) -> None:
    """
    Builds the main page.
    """
    try:
        reactor = Reactor(page)
        multiplexing_event = Event()
        multiplexing_event.set()
        
        # Run the multiplexing loop in a background thread managed by Flet.
        page.run_thread(loop_multiplexing, multiplexing_event, reactor)
        logger.info("Multiplexing thread started.")
        
        async def handle_close(event: ft.WindowEvent | None) -> None:
            if event is None or event.data == "close" or event.type == ft.WindowEventType.CLOSE:
               await close_page(multiplexing_event, page)
        
        page.window.on_event = handle_close
        page.window.prevent_close = True
        page.window.width = 800
        page.window.height = 600
        page.window.resizable = False
        page.theme_mode = ft.ThemeMode.DARK
        page.title = "RC-application"
        
        # Handles OS intrusions gracefully.
        # Similar to a regular container.
        reactor_client = ReactorClient(reactor)
        layout = Layout(lambda conn_data: add_conn(conn_data, reactor_client, layout))
        safe_area = ft.SafeArea(layout, expand=True)
        page.add(safe_area)
        logger.info("Flet app window initialized.")
    
    except Exception as e:
        logger.error(f"Application failed: {e}.", exc_info=True)
        page.run_task(page.window.close)

if __name__ == "__main__":
    if core.IS_CLI:
        raise NotImplementedError("CLI mode is not implemented yet")
    else:
        logger.info("GUI mode enabled.")
        ft.run(build_page, assets_dir="src/frontend/assets")

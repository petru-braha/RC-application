import flet as ft
from threading import Thread, Event
from time import sleep

from core import IS_CLI, get_logger
from frontend import Layout

from multiplexing import run_multiplexing_loop

logger = get_logger(__name__)

def main() -> None:

    def close_application() -> None:
        with open("demofile.txt", "a") as f:
            f.write("Now the file has more content!")
        try:
            multiplexing_event.clear()
            with open("demofile1111.txt", "a") as f:
                f.write("Now the file has more content!")
            sleep(2)
            multiplexing_thread.join()
            with open("demofile2222.txt", "a") as f:
                f.write("Now the file has more content!")
            logger.info("Closing application...")
        except BaseException as e:
            logger.error(f"Application failed: {e}.", exc_info=True)
        

    # Start a thread for the I/O multiplexing loop.
    logger.info("Starting application...")
    try:
        multiplexing_event = Event()
        multiplexing_thread = Thread(target=run_multiplexing_loop, args=[multiplexing_event])
        multiplexing_event.set()
        multiplexing_thread.start()
        logger.info("Multiplexing thread started.")
    
    except Exception as e:
        logger.critical(f"Thread failed: {e}.")
        close_application()
        exit()
    # Catch all exceptions (such as `KeyboardInterrupt`) to ensure that all resources are freed correctly.
    except BaseException as e:
        logger.critical(f"Application forcely closed: {e}.")
        close_application()
        exit()
    
    def build_page(page: ft.Page) -> None:
        page.on_close = close_application
        logger.info("Initializing Flet app window...")
        try:
            page.title = "RC-application"
            page.theme_mode = ft.ThemeMode.DARK
            # Handles OS intrusions gracefully.
            # Similar to a regular container.
            safe_area = ft.SafeArea(Layout(), expand=True)
            page.add(safe_area)
        
        except Exception as e:
            logger.error(f"Application failed: {e}.", exc_info=True)
            page.on_close()
        except BaseException as e:
            logger.error(f"Application forcely closed: {e}.", exc_info=True)
            page.on_close()
    
    if IS_CLI:
        raise NotImplementedError("CLI mode is not implemented yet")
        logger.info("CLI mode enabled.")
    else:
        logger.info("GUI mode enabled.")
        ft.run(build_page, assets_dir="src/frontend/assets")
    
if __name__ == "__main__":
    # Start the application loop.
    main()

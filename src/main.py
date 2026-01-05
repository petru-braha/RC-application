from threading import Thread, Event

from core import Config
from frontend import open_window

from reactor import close_application
from multiplexing import run_multiplexing_loop

logger = Config.get_logger(__name__)

def main() -> None:
    logger.info("Starting application...")
    
    try:
        # Start a thread for the I/O multiplexing loop.
        multiplexing_event = Event()
        multiplexing_thread = Thread(target=run_multiplexing_loop, args=[multiplexing_event])
        multiplexing_event.set()
        multiplexing_thread.start()
        logger.info("Multiplexing thread started.")

        # Start the application loop.
        if Config.cli:
            raise NotImplementedError("CLI mode is not implemented yet")
            logger.info("CLI mode enabled.")
        else:
            logger.info("GUI mode enabled.")
            open_window()

    except Exception as e:
        logger.critical(f"Application failed: {e}.", exc_info=True)
    finally:
        multiplexing_event.clear()
        multiplexing_thread.join()
        close_application()
        logger.info("Closing application...")

if __name__ == "__main__":
    main()

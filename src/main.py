from threading import Thread

from core import Config
from frontend import open_window

from reactor import close
from parallel_operator import run_multiplexing

logger = Config.get_logger(__name__)

def main() -> None:
    logger.info("Starting application...")
    
    try:
        # Starts another thread for the event loop.
        th = Thread(target=run_multiplexing, daemon=True)
        th.start()
        logger.info("Multiplexing event loop thread started.")

        # Start the GUI / CLI app loops.
        if Config.cli:
            raise NotImplementedError("CLI mode is not implemented yet.")
            logger.info("CLI mode enabled.")
        else:
            logger.info("GUI mode enabled.")
            open_window()

        # Wait for the event loop to finish.
        th.join()
    
    except Exception as e:
        logger.critical(f"Application failed: {e}", exc_info=True)
    finally:
        close()
        logger.info("Closing application...")
        exit()

if __name__ == "__main__":
    main()

from core import Config
from frontend import open_window

from parallel_operator import ParallelOperator

logger = Config.get_logger(__name__)

def main() -> None:
    logger.info("Starting application...")
    try:
        ParallelOperator.start()
        if Config.cli:
            raise NotImplementedError("CLI mode is not implemented yet.")
            logger.info("CLI mode enabled.")
        else:
            logger.info("GUI mode enabled.")
            open_window()
    except Exception as e:
        logger.critical(f"Application failed: {e}", exc_info=True)
    finally:
        try:
            ParallelOperator.close()
        except Exception as e:
            logger.error(f"Failed to close operator: {e}.")
        logger.info("Closing application...")

if __name__ == "__main__":
    main()

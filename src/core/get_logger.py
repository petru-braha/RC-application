import logging

from .config import FILE_HANDLER, STDOUT_HANDLER, STDERR_HANDLER

# The method that should be used by client modules.
def get_logger(name: str) -> logging.Logger:
    """
    Retrieves a configured logger instance.

    Attaches the standard file, stdout, and stderr handlers to the logger.

    Args:
        name (str): The name of the logger (usually __name__).

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    logger.addHandler(FILE_HANDLER)
    logger.addHandler(STDOUT_HANDLER)
    logger.addHandler(STDERR_HANDLER)

    return logger

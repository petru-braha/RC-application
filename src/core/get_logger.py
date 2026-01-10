import logging

from .config import STAGE, FILE_HANDLER, STDOUT_HANDLER, STDERR_HANDLER
from .constants import StageEnum

def get_logger(name: str) -> logging.Logger:
    """
    Retrieves a configured logger instance.

    Attaches the standard file, stdout, and stderr handlers to the logger.

    Args:
        name (str): The name of the logger (usually __name__).

    Returns:
        logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    logging_level = logging.INFO if STAGE == StageEnum.PROD else logging.DEBUG
    logger.setLevel(logging_level)

    logger.addHandler(FILE_HANDLER)
    logger.addHandler(STDOUT_HANDLER)
    logger.addHandler(STDERR_HANDLER)

    return logger

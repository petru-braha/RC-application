from enum import IntEnum
import logging
import sys

from structs import TruncatingLogFormatter

# Keep this as an enum since it can be extended to much more (e.g. testing).
class Stage(IntEnum):
    PROD = 0
    DEV = 1

# App and logging configuration.
# A log level has to be greater than the level of the handler in order to be printed.
# Making a hierarchy of loggers was considered but is far beyond the scope of this application.
class Config:
    """
    Centralized configuration manager for the application.

    Handles initialization of global settings, logging, and environment variables.
    Determines execution mode (CLI vs GUI) and manages connection parameters.
    """
    
    _CLI_FLAG: str = "--cli"
    """
    Internal flag used to detect CLI mode from command line arguments.
    """
    DEFAULT_MAX_CONNECTIONS: int = 1024
    """
    Default maximum limit of concurrent client connections.
    """
    DEFAULT_LOG_FILE: str = "./log/debug.log"
    """
    Default path for the log file.
    """

    VERBOSE_FORMAT: str = "%(asctime)s %(levelname)s - %(message)s --- %(name)s[%(lineno)d]"
    """
    Format string for verbose logging (used in file logs).
    """
    DANGER_FORMAT: str = "%(levelname)s - %(message)s --- %(name)s[%(lineno)d]"
    """
    Format string for warnings and errors logging.
    """
    SIMPLE_FORMAT: str = "%(levelname)s - %(message)s --- %(name)s"
    """
    Format string for simple logging (used in console output).
    """

    cli: bool
    """
    Indicates if the application is running in Command Line Interface mode.
    """
    stage: Stage
    """
    Current deployment stage (PROD, DEV, etc.).
    """
    tls_enforced: bool
    """
    Whether TLS encryption is enforced for connections.
    """
    max_connections: int
    """
    Maximum allowed concurrent connections.
    """
    
    file_handler: logging.Handler
    """
    Logging handler for writing debug logs to a file.
    """
    stdout_handler: logging.Handler
    """
    Logging handler for writing info loops to standard output.
    """
    stderr_handler: logging.Handler
    """
    Logging handler for writing warnings and errors to standard error.
    """

    @staticmethod
    def init(dotenv_dict: dict[str, str | None]) -> None:
        """
        Initializes the configuration static variables.

        Sets default values and overrides them with provided environment variables.
        Also configures the logging handlers.

        Parameters:
            dotenv_dict (dict): Dictionary containing environment variables.

        Raises:
            KeyError: If an invalid stage is provided in the environment variables.
        """
        Config.cli = len(sys.argv) > 1 and sys.argv[1] == Config._CLI_FLAG

        app_configs = [
            ("stage", Stage.DEV, lambda x: Stage[x]),
            ("tls_enforced", False, lambda x: str(x).lower() == "true"),
            ("max_connections", Config.DEFAULT_MAX_CONNECTIONS, int),
            ("file_handler", None, logging.FileHandler),
            ("stdout_handler", None, logging.StreamHandler),
            ("stderr_handler", None, logging.StreamHandler)
        ]
        for key, default, func in app_configs:
            if value := dotenv_dict.get(key):
                setattr(Config, key, func(value))
            else:
                setattr(Config, key, default)

        # Initialize handlers if they weren't overridden.
        if Config.file_handler == None:
             Config.file_handler = logging.FileHandler(Config.DEFAULT_LOG_FILE)
        if Config.stdout_handler == None:
             Config.stdout_handler = logging.StreamHandler(sys.stdout)
        if Config.stderr_handler == None:
             Config.stderr_handler = logging.StreamHandler(sys.stderr)

        Config.file_handler.setLevel(logging.DEBUG)
        Config.file_handler.setFormatter(logging.Formatter(Config.VERBOSE_FORMAT))
        Config.file_handler.addFilter(lambda r: r.levelno == logging.DEBUG)

        Config.stdout_handler.setLevel(logging.DEBUG)
        Config.stdout_handler.setFormatter(
            TruncatingLogFormatter(Config.SIMPLE_FORMAT, TruncatingLogFormatter.DEFAULT_MAX_BYTES / 4))
        Config.stdout_handler.addFilter(lambda r: r.levelno <= logging.INFO)
        
        Config.stderr_handler.setLevel(logging.WARNING)
        Config.stderr_handler.setFormatter(TruncatingLogFormatter(Config.DANGER_FORMAT))

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Retrieves a configured logger instance.

        Attaches the standard file, stdout, and stderr handlers to the logger.

        Parameters:
            name (str): The name of the logger (usually __name__).

        Returns:
            logging.Logger: The configured logger instance.
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        logger.addHandler(Config.file_handler)
        logger.addHandler(Config.stdout_handler)
        logger.addHandler(Config.stderr_handler)

        return logger

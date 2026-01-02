from enum import IntEnum
from sys import argv

# Keep this as an enum since it can be extended to much more (e.g. testing).
class Stage(IntEnum):
    PROD = 0
    DEV = 1

class Config:
    """
    Determines how the application was lauched, either with a GUI/CLI.
    Reads the content of the ".env" file (if present).
    If the file does not exist or some variables are missing, defaults them according to the basic values.
    """
    
    DEFAULT_MAX_CONNECTIONS: int = 1024
    """
    Default limit of client connections.
    """

    # Argument Parser python module interferences with flet.
    # A simple check upon sys.argv is enough.
    CLI_FLAG = "--cli"
    """
    Expected flag to be provided if the GUI mode is disabled.
    """

    def __init__(self, dotenv_dict: dict[str, str | None]) -> None:
        """
        Raises:
            KeyError: The stage string value is NOT from the "Stage" class.
        """
        self.cli = False
        self.stage = Stage.DEV
        self.tls_enforced = False
        self.max_connections = Config.DEFAULT_MAX_CONNECTIONS

        if len(argv) > 1 and argv[1] == Config.CLI_FLAG:
            self.cli = True
        
        # Raises KeyError if invalid.
        given_stage_str = dotenv_dict["stage"]
        self.stage = Stage[given_stage_str]

        given_tls_enforced = dotenv_dict["tls_enforced"]
        self.tls_enforced = given_tls_enforced == True
        
        max_connections = dotenv_dict["max_connections"]
        if max_connections:
            self.max_connections = max_connections

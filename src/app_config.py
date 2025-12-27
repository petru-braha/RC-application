from dotenv import dotenv_values
from enum import IntEnum

# Keep this as an enum since it can be extended to much more (e.g. testing).
class Stage(IntEnum):
    PROD = 0
    DEV = 1

def display_env_variables(filepath="./.env"):
    """
    Loads variables from a file and prints keys and values.
    """
    config = dotenv_values(filepath)
    
    if not config:
        print(f"Warning: No variables found in {filepath} (or file does not exist).")
        return

class AppConfig:
    
    _DEFAULT_CONN_LIMIT: int = 1024
    """
    Default limit of client connections.
    """

    _DOT_ENV_PATH: str = "./.env"
    """
    Default file path of the file.
    """

    def __init__(self,
                 stage: Stage = Stage.DEV,
                 tls_enforced: bool = False,
                 conn_count_limit: int = _DEFAULT_CONN_LIMIT):

        if conn_count_limit < 1:
            raise ValueError("Connection limit must be at least 1.")
        if conn_count_limit > AppConfig._DEFAULT_CONN_LIMIT:
            raise ValueError("Connection limit can not exceed 1024.")
        
        self.client_config = self.read_dot_env()

        self.stage = stage
        # This has to be determined in another way.
        self.gui_enabled = gui_enabled
        self.tls_enforced = tls_enforced
        self.conn_count_limit = conn_count_limit

    def read_dot_env(self):
        self.config = dotenv_values(AppConfig._DOT_ENV_PATH)
    
        if not self.client_config:
            # todo warning
            print(f"Warning: No variables found in {filepath} (or file does not exist).")




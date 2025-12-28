from constants import EMPTY_STR

from .identification import Identification

class DatabaseLink(Identification):
    
    DEFAULT_DB: int = 0
    """
    Default logical database of a Redis instance.
    """

    def __init__(self,
                 host: str,
                 port: str,
                 user: str,
                 pasw: str,
                 db_idx: str) -> None:
        super().__init__(host, port, user, pasw)
        if db_idx != DatabaseLink.DEFAULT_DB and db_idx == EMPTY_STR:
            self.say_select(db_idx)

    def say_select(self, db_idx):
        self.append_cmd(f"SELECT {db_idx}")

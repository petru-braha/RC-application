from constants import EMPTY_STR

from .identification import Identification

class DatabaseLink(Identification):
    """
    Manages the selection of the logical database in the Redis instance.
    Ensures the correct database index is selected upon connection.
    """
    
    # Strings were used instead of ints for two main reasons.
    # The received input is always a string (either from CLI/GUI).
    # Casting it to int does not provide any additional functionality.
    DEFAULT_DB: str = "0"
    """
    Default logical database of a Redis instance.
    """

    _SELECT_CMD: str = "SELECT"
    """
    Command automatically sent when connecting,
    used for selecting the provided logical database of a Redis server.
    """

    def __init__(self, host: str, port: str, user: str, pasw: str, db_idx: str) -> None:
        super().__init__(host, port, user, pasw)
        if db_idx != DatabaseLink.DEFAULT_DB and db_idx != EMPTY_STR:
            self._say_select(db_idx)

    def _say_select(self, db_idx: str) -> None:
        """
        Queues the SELECT command to switch to the specified database index.
        If the default database is selected, no action is taken.

        Parameters:
            db_idx (str): The index of the database to select.
        """
        self.add_pending(f"{DatabaseLink._SELECT_CMD} {db_idx}")

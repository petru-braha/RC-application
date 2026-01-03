from .database_link import DatabaseLink

# "Connection" is being kept as a separated class.
# If additional functionality is needed, it can be added here,
# rather than changing the super classes.
class Connection(DatabaseLink):
    """
    Manages the final step of the connection process.
    Acts as the primary interface for creating and maintaining a network connection.
    """

    # Host and port are internally converted into an Address object.
    # Clients might be interested in typing them manually, so they are kept as separated parameters.
    def __init__(self, host: str, port: str, user: str, pasw: str, db_idx: str) -> None:
        super().__init__(host, port, user, pasw, db_idx)

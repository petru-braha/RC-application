import core

from .database_link import DatabaseLink

logger = core.get_logger(__name__)

# "Connection" is being kept as a separated class.
# If additional functionality is needed, it can be added here,
# rather than changing the super classes.
class Connection(DatabaseLink):
    """
    Manages the final step of the connection process.
    Acts as the primary interface for creating and maintaining a network connection.
    """
    count: int = 0
    """
    The number of active connections.
    """
    
    # Host and port are internally converted into an Addr object.
    # Clients might be interested in typing them manually, so they are kept as separated parameters.
    def __init__(self, host: str, port: str, user: str, pasw: str, db_idx: str) -> None:
        if core.MAX_CONNECTIONS <= Connection.count:
            raise core.ConnectionCountError("Maximum number of connections reached.")
        
        logger.info(f"Initializing connection pipeline for {host}:{port}.")
        super().__init__(host, port, user, pasw, db_idx)
        Connection.count += 1
    
    def close(self) -> None:
        self.sock.close()
        Connection.count -= 1
    
    def __str__(self) -> str:
        return str(self.addr)

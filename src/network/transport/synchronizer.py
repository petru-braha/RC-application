# The principal usecase is to prevent recv() method calls when a pending input is not all sent.
# The secondary usecase is to debug client commands when handling output.
# E.g.: RC-application automatically sends HELLO and SELECT commands when a connection is established.
# It would be convenient to check their output. What if the remote server returns "HELLO - unkown command"?
class Synchronizer:
    """
    Socket I/O synchronization.

    Another input should not be sent until the previous one is all received.
    """

    def __init__(self) -> None:
        self.last_raw_input: str | None = None
        self.all_sent: bool | None = None
        self.all_recv: bool | None = None
    
    def sync_input(self, pending: str) -> None:
        """
        Syncs the input with the output.
        
        Args:
            pending (str): The pending input to sync.
        """
        self.last_raw_input = pending
        self.all_sent = False
        self.all_recv = False

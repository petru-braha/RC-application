from .network import Sock

from .types import History

class _AppState:
    """
    """
    
    # The order of the connections is important.
    # The insertion order is being kept for dictionaries in Python >= 3.7.
    # https://www.geeksforgeeks.org/python/ordereddict-in-python/
    _sock_hist_dict: dict[Sock, History] = {}
    """
    Keep the history of each socket.
    """

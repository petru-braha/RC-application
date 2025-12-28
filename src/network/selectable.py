import selectors

from core import SelectorHolder

from .transport import Sock

class Selectable(Sock):
    _EVENT_MASK = selectors.EVENT_READ | selectors.EVENT_WRITE
    """
    Default event mask to be carried within selection process.
    """

    def __init__(self) -> None:
        SelectorHolder.SELECTOR.register(self, Selectable._EVENT_MASK)

    def unregister(self) -> None:
        SelectorHolder.SELECTOR.unregister(self)

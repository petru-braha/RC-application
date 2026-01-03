from typing import Callable

from frontend import PresenceChangeable

from .modals import ManualMode, UrlMode

class ConnectModal(PresenceChangeable, ManualMode, UrlMode):
    def __init__(self, on_insert: Callable):
        ManualMode.__init__(self, on_insert)
        UrlMode.__init__(self, on_insert)
        self.set_url_mode()

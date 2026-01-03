from typing import Callable

from frontend import PresenceChangeable

from .modals import ManualMode, UrlMode

class ConnectModal(PresenceChangeable, ManualMode, UrlMode):
    """
    Handles the creation and the deletion of connections through the reactor.
    """

    def __init__(self, on_agenda_insert: Callable, on_agenda_remove: Callable, on_chat_insert: Callable):
        ManualMode.__init__(self, on_agenda_insert, on_agenda_remove, on_chat_insert)
        UrlMode.__init__(self, on_agenda_insert, on_agenda_remove, on_chat_insert)
        self.set_url_mode()

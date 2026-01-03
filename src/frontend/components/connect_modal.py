from typing import Callable

from frontend import PresenceChangeable

from .modals import ManualConnect, UrlMode

class ModalController(PresenceChangeable):
    """
    Handles the creation and the deletion of connections through the reactor.
    """

    def __init__(self, on_agenda_insert: Callable, on_agenda_remove: Callable, on_chat_insert: Callable, on_chat_remove: Callable):
        
        self.manual_modal = ManualConnect(on_agenda_insert, on_agenda_remove, on_chat_insert, on_chat_remove)
        self.url_modal = UrlMode(on_agenda_insert, on_agenda_remove, on_chat_insert, on_chat_remove)
        self.manual_modal.hide()
        self.url_modal.hide()

    def switch_modal(self, e):
        if self.manual_modal.visible:
            self.manual_modal.hide()
            self.url_modal.show()
        else:
            self.manual_modal.show()
            self.url_modal.hide()

    
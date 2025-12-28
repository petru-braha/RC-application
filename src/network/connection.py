from constants import EMPTY_STR

from core.reactor import Reactor

from .database_link import DatabaseLink
from .selectable import Selectable

class Connection(DatabaseLink, Selectable):

    # Here host and port are kept as parameterss,
    # but later will be converted into an Address object.
    # since clients might be intersted in typing them manually, can not generalize them.
    def __init__(self,
                 host: str = EMPTY_STR,
                 port: str = EMPTY_STR,
                 user: str = EMPTY_STR,
                 pasw: str = EMPTY_STR,
                 db_idx: str = EMPTY_STR) -> None:
        DatabaseLink.__init__(self, host, port, user, pasw, db_idx)
        Selectable.__init__(self)

    def destroy(self):
        self.unregister()
        self.try_close()

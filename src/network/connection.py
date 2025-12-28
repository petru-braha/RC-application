from constants import EMPTY_STR

from core.reactor import Reactor

from .database_link import DatabaseLink

class Connection(DatabaseLink):

    # Here host and port are kept as parameterss,
    # but later will be converted into an Address object.
    # since clients might be intersted in typing them manually, can not generalize them.
    def __init__(self,
                 host: str = EMPTY_STR,
                 port: str = EMPTY_STR,
                 user: str = EMPTY_STR,
                 pasw: str = EMPTY_STR,
                 db_idx: str = EMPTY_STR) -> None:
        super().__init__(host, port, user, pasw, db_idx)

    def destroy(self):
        Reactor.unregister(self)
        self.try_close()

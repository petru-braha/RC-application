from constants import EMPTY_STR

from .database_link import DatabaseLink

# While it currently doesn't add extra functionality,
# "Connection" is being kept is being kept as a separated class, 
# since implementation could be changed, rather than chaging the super classes.
class Connection(DatabaseLink):

    # Here host and port are kept as parameterss,
    # but later will be converted into an Address object.
    # since clients might be intersted in typing them manually, can not generalize them.
    def __init__(self, host: str, port: str, user: str, pasw: str, db_idx: str) -> None:
        super().__init__(self, host, port, user, pasw, db_idx)

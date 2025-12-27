from src.exceptions import RCException

#! network errors
class TransportError(RCException):
    MSG_PREFIX = "Transport exception"

class PartialResponseError(TransportError):
    pass

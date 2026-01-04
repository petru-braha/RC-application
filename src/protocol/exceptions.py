from core.exceptions import RCException

#! parser errors
class ParserError(RCException):
    MSG_PREFIX = "Parser exception"

class SpaceError(ParserError):
    pass

class QuoteError(ParserError):
    pass

from core.exceptions import RCError

#! parser errors
class ParserError(RCError):
    MSG_PREFIX = "Parser exception"

class SpaceError(ParserError):
    pass

class QuoteError(ParserError):
    pass

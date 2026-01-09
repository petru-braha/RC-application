import core

#! parser errors
class ParserError(core.RCError):
    MSG_PREFIX = "Parser exception"

class SpaceError(ParserError):
    pass

class QuoteError(ParserError):
    pass

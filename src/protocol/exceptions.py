from src.exceptions import RCException

#! parser errors
class ParserError(RCException):
    MSG_PREFIX = "Parser exception"

class SpaceError(ParserError):
    pass

class QuoteError(ParserError):
    pass

#! sanitizer errors
class SanitizerError(RCException):
    MSG_PREFIX = "Sanitizer exception"

class ArgumentCountError(SanitizerError):
    pass

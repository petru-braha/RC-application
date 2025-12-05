class RCException(Exception):
    MSG_PREFIX = "Redis Client Exception"
    
    def __str__(self) -> str:
        argc = len(self.args)
        msg = "Abstract error."
        if argc == 1:
            msg = self.args[0]
        elif argc > 1:
            msg = str(self.args)
        return self.MSG_PREFIX + " - " + msg

#! parser errors
class ParserError(RCException):
    MSG_PREFIX = "Parser exception"

class SpaceError(ParserError):
    pass

class QuoteError(ParserError):
    pass

#! sanitizer errors
class SanitizerError(RCException):
    MSG_PREFIX = "Sanitizer exception"

class ArgumentCountError(SanitizerError):
    pass

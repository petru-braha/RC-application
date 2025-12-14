class RCException(Exception):
    MSG_PREFIX = "Redis Client Exception"
    
    def __str__(self) -> str:
        argc = len(self.args)
        # If argc == 0 (an exception was raised with no arguments).
        msg = "Generic error with no message."
        if argc == 1:
            msg = self.args[0]
            if isinstance(msg, str) is False:
                msg = str(msg)
        elif argc > 1:
            msg = str(self.args)
        return self.MSG_PREFIX + " - " + msg

class AssignmentError(RCException):
    MSG_PREFIX = "Immutable Exception"

from core.exceptions import RCError

class TransmissionError(RCError):
    MSG_PREFIX = "Transmission Exception"

class Resp3NotSupportedError(TransmissionError):
    pass
    """
    Should be raised to signal that the server does not support RESP3,
    and that the client should retry with running the HELLO command with RESP2.
    """

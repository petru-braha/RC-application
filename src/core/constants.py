from enum import IntEnum

EMPTY_STR = ""
"""
Represents an empty string literal.
"""
EMPTY_LEN = 0
"""
How many elements are present in a empty container.
"""

SCHEME_LIST = ("redis", "rediss")
"""
Url connection supported schemes.
"""

ASCII_ENC = "ascii"
"""
"RESP is a binary protocol that uses control sequences encoded in standard ASCII."
https://redis.io/docs/latest/develop/reference/protocol-spec/
"""

CRLF = "\r\n"
"""
Standard RESP encoded data suffix.
"""

NOT_FOUND_INDEX = -1
"""
Returned by `find()` if the lookup value was not found.
"""

STR_TRAVERSAL_STRIDE = 1
"""
How many characters must be processed at once when traversing a string.
"""

class RespVer(IntEnum):
    """
    Redis Serialization Protocol supported versions.
    """

    RESP3 = 3
    RESP2 = 2
    """
    The stable version.
    """

# Keep this as an enum since it can be extended to much more (e.g. testing).
class StageEnum(IntEnum):
    PROD = 0
    DEV = 1

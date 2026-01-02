NOT_FOUND_INDEX = -1
"""
Returned by `find()` if the lookup value was not found.
"""

EMPTY_STR: str = ""
"""
Represents an empty string literal.
"""

STR_TRAVERSAL_STRIDE: int = 1
"""
How many characters must be processed at once when traversing a string.
"""

EMPTY_LEN: int = 0
"""
How many elements are present in a empty container.
"""

SCHEME_LIST: tuple[str, str] = ("redis", "rediss")
"""
Url connection supported schemes.
"""

ASCII_ENC: str = "ascii"
"""
"RESP is a binary protocol that uses control sequences encoded in standard ASCII."
https://redis.io/docs/latest/develop/reference/protocol-spec/
"""

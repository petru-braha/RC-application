from enum import IntEnum

# RESP data types pointing to their first byte in the RESP_SYMB array.
# The code usage looks as `RESP_SYMB[SIMPLE_STRINGS]`.
# Used when encoding user input.
# To not be confused with Redis data structures as they serve totally different purpose.
class RespDataType(IntEnum):
    SIMPLE_STRINGS = 0
    SIMPLE_ERRORS = 1
    INTEGERS = 2
    BULK_STRINGS = 3
    ARRAYS = 4
    NULLS = 5
    BOOLEANS = 6
    DOUBLES = 7
    BIG_NUMBERS = 8
    BULK_ERRORS = 9
    VERBATIM_STRINGS = 10
    MAPS = 11
    ATTRIBUTES = 12
    SETS = 13
    PUSHES = 14

# Predefined array of symbols containing the first byte of a RESP data type.
# See more: https://redis.io/docs/latest/develop/reference/protocol-spec/
RESP_SYMB = ( "+", "-", ":", "$", "*", "_", "#", ",", "(", "!", "=", "%", "|", "~", ">" )

# Predefined dictionary mapping the first byte of an incoming Redis response to its data type index.
# See more: https://redis.io/docs/latest/develop/reference/protocol-spec/
SYMB_TYPE = {symb: idx for idx, symb in enumerate(RESP_SYMB)}

# Standard RESP encoded data suffix.
CRLF = "\r\n"

# Standard input string constant.
SPACE = " "
QUOTE_DOUBLE = "\""
QUOTE_SINGLE = "\'"

# See more: https://redis.io/docs/latest/develop/tools/cli/
QUOTE_STATES = dict()
# Supported escape sequences: \", \n, \r, \t, \b, \a, \\, \xhh
QUOTE_STATES[QUOTE_DOUBLE] = {
    "\"": "\"",
    "n": "\n",
    "r": "\r",
    "t": "\t",
    "b": "\b",
    "a": "\a",
    "\\": "\\",
    # "xhh": "\xhh"
    # Unsupported escape sequence in string literalPylancereportInvalidStringEscapeSequence
}
# Supported escape sequences: \', \\
QUOTE_STATES[QUOTE_SINGLE] = {
    "\'": "\'",
    "\\": "\\"
}

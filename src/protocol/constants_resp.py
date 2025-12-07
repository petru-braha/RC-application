from enum import IntEnum
from frozendict import frozendict

class RespDataType(IntEnum):
    """
    RESP data types pointing to their first byte in the RESP_SYMB array.
    Used when encoding user input.
    
    The code usage looks as `RESP_SYMB[SIMPLE_STRINGS]`.
    
    To not be confused with Redis data structures as they serve totally different purpose.
    """
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

RESP_SYMB = ( "+", "-", ":", "$", "*", "_", "#", ",", "(", "!", "=", "%", "|", "~", ">" )
"""
Predefined array of symbols containing the first byte of a RESP data type.

See more: https://redis.io/docs/latest/develop/reference/protocol-spec/
"""

SYMB_TYPE = frozendict({symb: idx for idx, symb in enumerate(RESP_SYMB)})
"""
Predefined dictionary mapping the first byte of an incoming Redis response to its data type index.

See more: https://redis.io/docs/latest/develop/reference/protocol-spec/
"""

# Standard input string constant.
SPACE = " "
QUOTE_DOUBLE = "\""
QUOTE_SINGLE = "\'"
NULL = "null"
"""
Standard RESP encoded data suffix.
"""

QUOTE_STATES = frozendict({
    # Supported escape sequences: \", \n, \r, \t, \b, \a, \\, \xhh.
    QUOTE_DOUBLE: frozendict({
        "\"": "\"",
        "n": "\n",
        "r": "\r",
        "t": "\t",
        "b": "\b",
        "a": "\a",
        "\\": "\\",
        # "xhh": "\xhh"
        # Unsupported escape sequence in string literal.
        # Pylance - reportInvalidStringEscapeSequence
    }),
    # Supported escape sequences: \', \\.
    QUOTE_SINGLE: frozendict({
        "\'": "\'",
        "\\": "\\"
    })
})
"""
Predefined dictionary for translating escape sequences.
When the parser reads a backslash, it checks the next character here.
If it exists in this map, the corresponding escaped value is produced.

See more: https://redis.io/docs/latest/develop/tools/cli/
"""

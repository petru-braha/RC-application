# A convention used in this project:
# Tackled Redis data structures are represented by integers.
# This design can be observed in multiple areas in the source code.
# The primary benefit is efficiency in storage, comparison, and lookup operations, as well as simplified type handling in functions like command validation and encoding.

from .types import *
from .string_cmds import STRING_CMDS
from .list_cmds import LIST_CMDS
from .set_cmds import SET_CMDS
from .hash_cmds import HASH_CMDS
from .sorted_set_cmds import SORTED_SET_CMDS
from .connection_cmds import CONNECTION_CMDS
from .generic_cmds import GENERIC_CMDS

CMDS = (STRING_CMDS, LIST_CMDS,
        SET_CMDS, HASH_CMDS, SORTED_SET_CMDS,
        CONNECTION_CMDS, GENERIC_CMDS)
"""
All comands in a single variable.
"""

__all__ = ["Arg", "IntArg", "FltArg", "StrArg",
           "Args", "Opts", "OptSet", "CmdDict",
           "CMDS", "STRING_CMDS", "LIST_CMDS",
           "SET_CMDS", "HASH_CMDS", "SORTED_SET_CMDS",
           "CONNECTION_CMDS", "GENERIC_CMDS"]

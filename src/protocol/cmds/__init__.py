from .patterns import *
from .connection_cmds import CONNECTION_CMDS
from .generic_cmds import GENERIC_CMDS
from .string_cmds import STRING_CMDS
from .list_cmds import LIST_CMDS
from .set_cmds import SET_CMDS
from .hash_cmds import HASH_CMDS
from .sorted_set_cmds import SORTED_SET_CMDS

CMDS = (CONNECTION_CMDS, GENERIC_CMDS,
        STRING_CMDS, LIST_CMDS,
        SET_CMDS, HASH_CMDS, SORTED_SET_CMDS)
"""
All comands in a single variable.
"""

__all__ = ["RequiredPattern", "OptionalPattern", "StrictPattern",
           "Argument",
           "ArgEzz", "ArgInt", "ArgFlt", "ArgStr", "ArgSet", "VariadicKey",
           
           "Section",
           "RequiredSect", "Vitals",
           "OptionalSect", "Optionals", "KeyedOptionals",
           "Opts", "Opts", "Variadic", "KdVariadic", "OptSet",
           
           "CMDS",
           "STRING_CMDS", "LIST_CMDS",
           "SET_CMDS", "HASH_CMDS", "SORTED_SET_CMDS",
           "CONNECTION_CMDS", "GENERIC_CMDS"]

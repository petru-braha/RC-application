from frozendict import frozendict
from .constraints_section import ArgConstrSect

# Mapping from option keyword to needed value count.
OptKeys = frozenset[str]

# Mapping from command name to its definition/constraints.
CmdDict = frozendict[str, tuple[ArgConstrSect]]

from frozendict import frozendict

from .core.constants import *
from .interfaces import *
from .sections import *
from .types import *

"""
Although Python does not natively enforce strict interfaces or abstract classes,
identifying them in documentation clarifies the architectural intent. These
annotations define the expected contract for the client, guiding usage despite
the absence of runtime constraints.

In this design, interfaces and abstract base classes serve as structural foundations
and must not be instantiated directly.

Interfaces define the semantic contract—establishing type roles, behavioral 
expectations, and validation boundaries that implementing classes must respect.
Conversely, abstract classes encapsulate shared logic and state to minimize 
redundancy across concrete implementations.
"""

# Mapping from command name to its definition/constraints.
CmdDict = frozendict[str, tuple[Section]]

# Default __all__ is good enough in here.
# No members need hiding.

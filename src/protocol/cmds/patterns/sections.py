from src.immutable import Immutable

from .interfaces import RequiredPattern, OptionalPattern
from .types import OptKey

class Section(Immutable):
    """
    Interface for a high-level command syntax section.
    
    Represents a logical grouping of patterns (arguments or options) that
    form a distinct part of a command's structure.
    """
    pass

class RequiredSect(Section):
    """
    Interface for a mandatory syntax section.
    
    All of its element must be both present and valid.
    """
    pass

class Vitals(RequiredSect):
    """
    Represents the core sequence of mandatory arguments.
    
    This section encapsulates the essential arguments required by a command,
    defined as an **ordered** tuple of patterns.
    
    Attributes:
        patterns (arr): The ordered sequence of required patterns.
    """
    def __init__(self, *patterns: RequiredPattern) -> None:
        super().__init__()
        self.patterns = tuple(patterns)

class OptionalSect(Section, OptionalPattern):
    """
    Interface for an optional syntax section.
    
    Represents a segment of the command that can be omitted. Inherits from 
    OptionalPattern to allow nesting within other optional structures.
    """
    pass

class Optionals(OptionalSect):
    """
    Base abstract class for a collection of optional patterns.
    
    Attributes:
        patterns (arr): A sequence of patterns 
            contained within this optional section.
    """
    def __init__(self, patterns: tuple[OptionalPattern, ...]) -> None:
        super().__init__()
        self.patterns = patterns

class Opts(Optionals):
    """
    Represents a linear sequence of optional arguments.
    
    Used for standard optional segments that do not require a specific 
    prefixing key (flag).
    """
    def __init__(self, *patterns: OptionalPattern) -> None:
        super().__init__(tuple(patterns))

class Variadic(Opts):
    """
    Represents a variadic sequence of optional arguments.
    
    Used for optional segments where the defined patterns can be repeated 
    multiple times (typically handling "one or more" or "zero or more" logic).
    
    When initialized with multiple patterns, the accepted input acts as a 
    repeating cycle of that sequence. For example, if defined with three patterns, 
    the command accepts an unlimited number of arguments in groups of three, 
    where each argument in a group must match its corresponding pattern definition.
    """
    def __init__(self, *patterns: OptionalPattern) -> None:
        super().__init__(*patterns)

class KeyedOptionals(Optionals):
    """
    Abstract base class for optional arguments prefixed by a specific key.
    
    Represents options that consist of a strict identifier (e.g., a flag 
    like 'LIMIT') followed by one or more associated values.

    The subclasses contain an additional layer of validation.
    For instance, if the client input contains the key,
    then the other section patterns are expected to be observed as well.
    
    Attributes:
        key (OptKey): The strict pattern acting as the identifier/flag.
    """
    def __init__(self, key: OptKey,
                 patterns: tuple[OptionalPattern, ...]) -> None:
        super().__init__(patterns)
        self.key = key

class KdOpts(KeyedOptionals):
    """
    Represents a keyed option with a fixed sequence of arguments.
    
    Example: 'LIMIT <offset> <count>' where 'LIMIT' is the key and 
    offset/count are the patterns.
    """
    def __init__(self, key: OptKey,
                 *patterns: OptionalPattern) -> None:
        super().__init__(key, tuple(patterns))

class KdVariadic(KdOpts):
    """
    Represents a keyed option that accepts a variadic number of arguments.
    
    Example: A flag followed by an arbitrary list of values.
    """
    def __init__(self, key: OptKey,
                 *patterns: OptionalPattern) -> None:
        super().__init__(key, *patterns)

class OptSet(OptionalSect):
    """
    Represents a set of independent keyed options.
    
    Used for groups of options where order is irrelevant, or to define 
    mutually exclusive sets of flags.
    
    Attributes:
        patterns (set): An immutable set of available keyed options.
    """
    def __init__(self, *kd_opts: KeyedOptionals) -> None:
        super().__init__()
        self.patterns = frozenset(kd_opts)

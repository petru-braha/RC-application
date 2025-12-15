from .interfaces import RequiredPattern, OptionalPattern, StrictPattern

class Argument(RequiredPattern, OptionalPattern):
    """
    Interface for a singel command argument.
    
    Represents a generic input unit that can function as either a required
    or an optional component within a command structure. Subclasses define
    specific data types or matching logic (e.g., integers, literals).
    """
    pass

class ArgEzz(Argument):
    """
    Represents an argument with no restrictions.
    
    Used for variable inputs (such as keys or arbitrary string values) 
    that do not need to match a specific pre-defined pattern/keyword.
    """
    pass

class ArgInt(Argument):
    """
    Represents an integer argument.
    
    Validates that the provided input token can be parsed as an integer.
    """
    pass

class ArgFlt(Argument):
    """
    Represents a floating-point argument.
    
    Validates that the provided input token can be parsed as a float.
    """
    pass

class ArgStr(Argument, StrictPattern):
    """
    Represents a strict string literal argument (Keyword).
    
    Used for command flags or keywords that must match a specific string
    pattern exactly.
    
    Attributes:
        pattern (str): The exact string literal that this argument matches.
    """
    def __init__(self, pattern: str) -> None:
        super().__init__()
        self.pattern = pattern

class ArgSet(Argument, StrictPattern):
    """
    Represents a set of mutually exclusive string literal arguments.
    
    Used when an argument must match exactly one of a provided set of
    allowed keywords (similar to an Enum).
    
    Attributes:
        patterns (frozenset): An immutable set of allowed string patterns.
    """
    def __init__(self, *patterns: str) -> None:
        super().__init__()
        self.patterns = frozenset({patterns})

class OptKey(StrictPattern):
    """
    Represents a prefix component for option sections.
    
    Wraps a strict pattern that serves as the identifier
    for a key-value pair in an optional section (e.g., 'LIMIT' in 'LIMIT 10').
    
    Attributes:
        pattern (StrictPattern): The strict pattern acting as the option key.
    """
    def __init__(self, pattern: StrictPattern) -> None:
        self.pattern = pattern

from immutable import Immutable

class RequiredPattern(Immutable):
    """
    Interface representing a mandatory pattern.
    
    This interface serves as a marker for pattern types that must be satisfied
    for a section or argument list to be considered valid. It ensures that
    subclasses are treated as required components during parsing or validation.
    """
    pass

class OptionalPattern(Immutable):
    """
    Interface representing a pattern that is optional.
    
    This interface serves as a marker for pattern types that do not strictly
    require a match. Subclasses represent arguments or structures that may 
    be omitted from the input without causing validation errors.
    """
    pass

class StrictPattern(Immutable):
    """
    Interface representing a pattern with strict matching constraints.
    
    This interface marks patterns that require exact validation logic, such as
    literal string matches or specific sets of allowed values, as opposed to
    looser, type-based matching (like integers or floats).
    """
    pass

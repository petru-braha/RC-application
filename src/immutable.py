from typing import Any

from .exceptions import AssignmentError

class Immutable:
    """
    A base class that enforces write-once immutability for its attributes.

    This class overrides `__setattr__` to ensure that attributes can only be
    set once (during initialization).
    Any attempt to modify an existing attribute will raise an exception.

    Usage:
        Inherit from this class to make your objects immutable after 
        their `__init__` method completes.

    Example:
        >>> class Point(Immutable):
        ...     def __init__(self, x, y):
        ...         self.x = x
        ...         self.y = y
        ...
        >>> p = Point(1, 2)
        >>> p.x
        1
        >>> p.x = 3
        Immutable Exception: Cannot modify 'x'.
    """

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Sets the value of an attribute only if it does not already exist.
        
        Raises:
            AssignmentError: If the attribute `name` already exists on the instance.
        """
        try:
            # Should throw AttributeError when initializing.
            _ = self.__getattribute__(name)
            # If the attribute already exists (was created by constructor),
            # then the immutability property tried to be violated.
            raise AssignmentError(f"Cannot modify '{name}'.")
        except AttributeError:
            # If __getattribute__ raises AttributeError, the attribute is missing.
            # Therefore allow the construction of the object.
            super().__setattr__(name, value)

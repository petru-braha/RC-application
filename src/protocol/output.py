"""
Output classes for representing decoded Redis RESP3/RESP2 data.

These classes provide a structured representation of data returned by the Redis server.
They allow recursive nesting to capture arrays, sets, and maps, preserving the hierarchical
nature of the responses.

OutputType = str | list[OutputType] | dict[OutputType, OutputType] | OutputType, OutputType
"""

from dataclasses import dataclass
from frozendict import frozendict
from typing import Callable

class Output:
    """
    Base class for all decoded Redis output types.

    Acts as a common ancestor for all RESP3 decoded values.

    Note: The stored data is immutable.
    """
    _callback: Callable | None = None

    def __str__(self) -> str:
        if Output._callback is None:
            from .formatter import formatter
            Output._callback = formatter
        return Output._callback(self)

@dataclass(frozen=True)
class OutputStr(Output):
    """
    Represents a simple string or scalar value returned by Redis.
    """
    value: str

@dataclass(frozen=True)
class OutputErr(Output):
    """
    Represents a RESP error (simple or bulk).
    """
    value: str

@dataclass(frozen=True)
class OutputSeq(Output):
    """
    Represents a list-like collection of Redis outputs (arrays, sets, or pushes).
    """
    values: tuple[Output, ...]

@dataclass(frozen=True)
class OutputMap(Output):
    """
    Represents a key-value mapping of Redis outputs.
    """
    values: frozendict[Output, Output]

@dataclass(frozen=True)
class OutputAtt(Output):
    """
    Represents a value decorated with attributes.
    """
    attributes: OutputMap
    payload: Output

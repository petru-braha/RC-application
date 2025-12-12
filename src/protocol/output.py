from frozendict import frozendict

"""
Output classes for representing decoded Redis RESP3/RESP2 data.

These classes provide a structured representation of data returned by the Redis server.
They allow recursive nesting to capture arrays, sets, and maps, preserving the hierarchical
nature of the responses.

OutputType = str | list[OutputType] | dict[OutputType, OutputType]
"""

class Output:
    """
    Base class for all decoded Redis output types.

    Acts as a common ancestor for all RESP3 decoded values.

    Note: The stored data is immutable.
    """
    pass

class OutputStr(Output):
    """
    Represents a simple string or scalar value returned by Redis.

    Attributes:
        value (str): The decoded string value.
    """
    def __init__(self, value: str) -> None:
        self.value = value

class OutputList(Output):
    """
    Represents a list-like collection of Redis outputs (arrays, sets, or pushes).

    Attributes:
        values (list[Output]): A list of decoded `Output` objects.
    """
    def __init__(self, values: tuple[Output, ...]) -> None:
        super().__init__()
        self.values = values

class OutputDict(Output):
    """
    Represents a key-value mapping of Redis outputs (maps or attributes).

    Attributes:
        values (dict[Output, Output]): A dictionary of decoded `Output` objects.
    """
    def __init__(self, values: frozendict[Output, Output]) -> None:
        super().__init__()
        self.values = values

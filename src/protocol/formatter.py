from src.constants import EMPTY_STR, STRING_TRAVERSAL_STRIDE

from .constants_resp import CRLF
from .output import Output, OutputStr, OutputSeq, OutputMap, OutputAtt

def formatter(output: Output, prefix: str = EMPTY_STR) -> str:
    """
    Formats a decoded RESP Output object into a human-readable string.

    Entry point for traversal.
    Dispatches aggregate types to their specific formatting methods.

    Parameters:
        output: The Output object (Str, Seq, Map, or Att) to format.
        prefix (str): Optional indentation string. Defaults to empty string.

    Returns:
        str: The fully formatted, human-readable string representation of the output.

    Raises:
        AssertionError: If the output type is NOT one of the expected Output subclasses.
    """
    # Strings (leaf nodes). No recursive calls are performed here.
    if isinstance(output, OutputStr):
        return _format_str(output.value, prefix)
    
    # Aggregate types. Potentially contain recursive calls.
    if isinstance(output, OutputSeq):
        return _format_seq(output, prefix)
    if isinstance(output, OutputMap):
        return _format_map(output, prefix)
    assert isinstance(output, OutputAtt)
    return _format_att(output, prefix)

_PAIR_SIZE: int = 2
"""
Internal constant.

Defines the number of items in a key-value pair (key + value).
Used for calculating indices in map formatting.
"""

_INDENT_CHAR: str = " "
"""
Internal constant.

Represents a single space character used for indentation padding.
"""

_EMPTY_SEQ_MSG: str = "(empty sequence)"
"""
Internal constant.

Message displayed when formatting an empty sequence output.
"""

_EMPTY_MAP_MSG: str = "(empty map)"
"""
Internal constant.

Message displayed when formatting an empty map output.
"""

_ATTR_HEADER: str = "Attributes:"
"""
Internal constant.

Header text displayed before the attributes section of an Attributed output.
"""

_PAYLOAD_HEADER: str = "Payload:"
"""
Internal constant.

Header text displayed before the payload section of an Attributed output.
"""

def _set_prefix(prefix: str, idx: int) -> str:
    """
    Internal method.

    Constructs a numbered prefix string for list items.

    Parameters:
        prefix (str): The existing indentation or parent prefix.
        idx (int): The current item index to display.

    Returns:
        str: The formatted prefix string ending with a closing parenthesis and space.
    """
    return f"{prefix}{idx}) "

def _format_str(output: str, prefix: str) -> str:
    """
    Internal method.

    Formats a simple string output by appending a newline.

    Parameters:
        output (str): The string content to format.
        prefix (str): The indentation string to prepend.

    Returns:
        str: The indented string followed by CRLF.
    """
    return prefix + output + CRLF

def _format_seq(output: OutputSeq, prefix: str) -> str:
    """
    Internal method.

    Formats a sequence (Array/Set/Push) into a numbered list.
    Handles empty sequences by returning a specific empty message.

    Parameters:
        output: The OutputSeq object containing the list of values.
        prefix (str): The indentation string for the current level.

    Returns:
        str: A multi-line string representing the numbered sequence.
    """
    values_len = len(output.values)
    if values_len < 1:
        return _format_str(_EMPTY_SEQ_MSG, prefix)
    
    # Handle the first element separately to apply the parent prefix.
    first_value = output.values[0]
    val_prefix = _set_prefix(prefix, 1)
    formatted = formatter(first_value, val_prefix)

    # Prepare indentation and iterate over subsequent elements.
    indent_padding = _INDENT_CHAR * len(prefix)
    
    for idx in range(1, values_len):
        value = output.values[idx]
        display_idx = idx + STRING_TRAVERSAL_STRIDE
        val_prefix = _set_prefix(indent_padding, display_idx)
        formatted += formatter(value, val_prefix)
    
    return formatted

def _format_map(output: OutputMap, prefix: str) -> str:
    """
    Internal method.

    Formats a Map into a flattened key-value list structure.
    Iterates through dictionary items and presents them as sequential numbered entries.

    Parameters:
        output: The OutputMap object containing key-value pairs.
        prefix (str): The indentation string for the current level.

    Returns:
        str: A multi-line string representing the flattened map.
    """
    values_len = len(output.values)
    if values_len < 1:
        return _format_str(_EMPTY_MAP_MSG, prefix)

    formatted = EMPTY_STR
    # Indentation for all pairs except the first one.
    indent_padding = _INDENT_CHAR * len(prefix)

    for idx, (key, val) in enumerate(output.values.items()):
        # Determine prefix for the Key:
        # If it's the very first key (idx == 0), use the parent 'prefix'.
        # Otherwise, use the calculated indentation padding.
        key_prefix = prefix if idx == 0 else indent_padding
        display_idx = idx * _PAIR_SIZE

        # Format Key.
        display_idx += STRING_TRAVERSAL_STRIDE
        key_prefix = _set_prefix(key_prefix, display_idx)
        formatted += formatter(key, key_prefix)

        # Format Value.
        display_idx += STRING_TRAVERSAL_STRIDE
        val_prefix = _set_prefix(indent_padding, display_idx)
        formatted += formatter(val, val_prefix)

    return formatted

def _format_att(output: OutputAtt, prefix: str) -> str:
    """
    Internal method.

    Formats an attribute based output.
    It is formed out of an attribute map and a payload,
    which can be any output type.

    Parameters:
        output: The OutputAtt object containing attributes and payload.
        prefix (str): The indentation string for the current level.

    Returns:
        str: A multi-line string separating attributes and payload with headers.
    """
    # Ignore empty attribute maps.
    if len(output.attributes.values) < 1:
        return formatter(output.payload, prefix)

    indent_padding = _INDENT_CHAR * len(prefix)
    formatted = _format_str(_ATTR_HEADER, indent_padding)
    formatted += _format_map(output.attributes, indent_padding)
    formatted += _format_str(_PAYLOAD_HEADER, indent_padding)
    # All of the above strings are considered additional.
    # It should not use the actual prefix.
    formatted += formatter(output.payload, prefix)
    return formatted

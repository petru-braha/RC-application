import core

from .constants_resp import SPACE, QUOTE_DOUBLE, QUOTE_SINGLE, QUOTE_TYPE
from .exceptions import QuoteError, SpaceError

_MIN_CMD_LEN: int = 3
"""
Minimum length of a valid input string.
"""

def parser(input: str) -> tuple[str, list[str]]:
    """
    Parses the input string into a list of tokens.

    Args:
        input (str): The raw input command string from the user.

    Returns:
        str: The command string.
        list[str]: An array containing each argument from the input.

    Raises:
        ValueError: If the input is empty.
        ParseError: In case of parsing errors related to either argument separators or quoting.
    """
    input_len = len(input)

    # All commands have a length greater of equal to 3.
    if input_len < _MIN_CMD_LEN:
        raise ValueError("The input string must contain at least one (supported) command")
    
    # Skip first idx spaces.
    idx = 0
    while idx < input_len and input[idx] == SPACE:
        idx += core.STR_TRAVERSAL_STRIDE
    
    space_idx = input.find(SPACE, idx)
    
    # Assume that there is only one token - the command.
    # str.find() returns -1 if the substring is not found.
    # The command is updated if a white space was found.
    if space_idx == core.NOT_FOUND_INDEX:
        return input[idx:input_len], []
    
    cmd = input[idx:space_idx]

    # space_idx + 1 == next position of a potential non-white-space char.
    parser = _ArgumentParser(input, space_idx + 1)
    return cmd, parser.argv

class _ArgumentParser:
    """
    Internal helper class.

    Parses raw input strings into structured command and argument components,
    managing state traversal internally.
    """
    
    _ESCAPE_CHAR: str = "\\"
    """
    Character used for escaping.
    """

    def __init__(self, input: str, start_idx: int) -> None:
        self._input = input
        self._input_len = len(input)
        self._idx = start_idx
        self.argv = self._get_argv()

    def _get_argv(self) -> list[str]:
        """
        Internal method.
        
        Extracts the list of arguments from the current index onwards.
        
        Returns:
            list[str]: The list of parsed argument strings.
        """
        argv = list()
        while self._idx < self._input_len:
            self._traverse_spaces()

            # Stop if end of input is reached after spaces.
            if self._idx == self._input_len:
                break
            arg = self._traverse_arg()
            
            # Verify valid separation if not at the end of the string.
            if self._idx < self._input_len and self._input[self._idx] != SPACE:
                raise SpaceError("Arguments must be separated by space")
            argv.append(arg)
            
        return argv
    
    def _traverse_spaces(self) -> None:
        """
        Internal method.
        
        Advances the internal index past any sequence of spaces.
        """
        while self._idx < self._input_len and self._input[self._idx] == SPACE:
            self._idx += core.STR_TRAVERSAL_STRIDE

    def _traverse_arg(self) -> str:
        """
        Internal method.
        
        Dispatches parsing to either quoted or unquoted logic based on the current character.
        
        Returns:
            str: The parsed argument.

        Raises:
            QuoteError: For quote parsing errors.
        """
        char = self._input[self._idx]
        if char == QUOTE_DOUBLE or char == QUOTE_SINGLE:
            # Skip the starting quote character.
            self._idx += core.STR_TRAVERSAL_STRIDE
            return self._visit_quoted(char)
        return self._visit_unquoted()

    def _visit_quoted(self, QUOTE: str) -> str:
        """
        Internal method.
        
        Parses a quoted argument, handling escape sequences.
        
        Args:
            QUOTE (str): The specific quote character (single or double) starting the sequence.

        Returns:
            str: The parsed string content with escape sequences resolved.

        Raises:
            QuoteError: If a second quote of the same type as the starting one was NOT found.
        """
        arg = core.EMPTY_STR
        while self._idx < self._input_len:
            char = self._input[self._idx]

            # Found the second quote, of the same type as the starting one.
            if char == QUOTE:
                self._idx += core.STR_TRAVERSAL_STRIDE
                return arg

            if char != _ArgumentParser._ESCAPE_CHAR:
                arg += char; self._idx += core.STR_TRAVERSAL_STRIDE; continue
            
            if self._idx + core.STR_TRAVERSAL_STRIDE == self._input_len:
                arg += char; self._idx += core.STR_TRAVERSAL_STRIDE; continue
            
            # If the "\\" byte was encountered check if the next character can escape.
            next_char = self._input[self._idx + core.STR_TRAVERSAL_STRIDE]
            escaped = QUOTE_TYPE[QUOTE].get(next_char)
            if escaped is not None:
                arg += escaped
            else:
                arg += (char + next_char)
            self._idx += 2 * core.STR_TRAVERSAL_STRIDE
        
       # Raised if an argument like "abc' is provided.
        raise QuoteError("Argument was not ended with a (correct) quote")

    def _visit_unquoted(self) -> str:
        """
        Internal method.
        
        Parses a standard argument until a space or end of string is encountered.

        Returns:
            str: The parsed argument string.

        Raises:
            QuoteError: If a quote is encountered (they should NOT be present).
        """
        arg = core.EMPTY_STR
        while self._idx < self._input_len:
            char = self._input[self._idx]
            
            if char == QUOTE_DOUBLE or char == QUOTE_SINGLE:
                raise QuoteError("Unquoted values must NOT contain quotes")

            if char == SPACE:
                return arg
            arg += char
            self._idx += core.STR_TRAVERSAL_STRIDE

        return arg

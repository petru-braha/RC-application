from src.constants import NOT_FOUND_INDEX

from .constants_resp import SPACE, QUOTE_DOUBLE, QUOTE_SINGLE, QUOTE_STATES
from .exceptions import QuoteError, SpaceError

def _visit_quoted(input: str, start_idx: int, QUOTE: str) -> tuple[str, int]:
    """
    Internal method.

    Returns:
        str: The parsed argument which could contain spaces or escaped characters.
        int: The index of the end delimiter (second quote).

    Raises:
        QuoteError: If a second quote of the same type as the starting one was NOT found.
    """
    arg = ""
    input_len = len(input)

    idx = start_idx
    while idx < input_len:

        char = input[idx]
        # Found the second quote, of the same type as the starting one.
        if char == QUOTE:
            return arg, idx

        if char != "\\":
            arg += char; idx += 1; continue
        
        if idx + 1 == input_len:
            arg += char; idx += 1; continue
        
        # If the "\\" byte was encountered check if the next character can escape.
        next = input[idx + 1]
        escaped = QUOTE_STATES[QUOTE].get(next)
        if escaped != None:
            arg += escaped
        else:
            arg += (char + next)
        idx += 2
    
    # Raised if an argument like "abc' is provided.
    raise QuoteError("Argument was not ended with a (correct) quote")

def _visit_unquoted(input: str, start_idx: int) -> tuple[str, int]:
    """
    Internal method.
    
    Returns:
        str: The parsed argument with no special characters (spaces, escaped).
        int: The index of the next space (argument separator).

    Raises:
        QuoteError: If a quote is encountered (they should NOT be present).
    """
    arg = ""
    input_len = len(input)
    for idx in range(start_idx, input_len):
        char = input[idx]
        if char == QUOTE_DOUBLE or char == QUOTE_SINGLE:
            raise QuoteError("Unquoted values must NOT contain quotes.")

        if char == SPACE:
            return arg, idx
        arg += char

    return arg, input_len

def _traverse_arg(input: str, start_idx: int) -> tuple[str, int]:
    """
    Internal method.
    Traverses an quoted/unquoted argument until its end delimiter (which can be either a space or a quote)

    Returns:
        str: The parsed argument.
        int: The index of the next space (argument separator).
    
    Raises:
        QuoteError: For quote parsing errors.
    """
    char = input[start_idx]
    if char == QUOTE_DOUBLE or char == QUOTE_SINGLE:
       # start_idx + 1 skips the starting quote character.
       # idx_new + 1 skips the ending quote character.
        arg, idx_new = _visit_quoted(input, start_idx + 1, char)
        return arg, idx_new + 1
    return _visit_unquoted(input, start_idx)

def _traverse_spaces(input: str, start_idx: int) -> int:
    """
    Internal method.
    Ignores all spaces.

    Returns:
        int: the index of a non-space character or the length of the string if the end is reached.
    """
    input_len = len(input)
    for idx in range(start_idx, input_len):
        if input[idx] != SPACE:
            return idx
    return input_len

def _get_argv(input: str, start_idx: int) -> list[str]:
    """
    Internal method.
    Extract command arguments from an input string.

    This function parses the substring of `input` beginning at `start_idx`,
    splitting it on space characters and returning the resulting tokens.

    Parameters:
        input (str): The full input string containing a command and its arguments.
        start_idx (int): The index in `input` from which argument parsing should begin.

    Returns:
        list[str]: A list of argument strings. Can be empty.
    
    Raises:
        SpaceError: If the arguments are not separated by a space.
        QuoteError: For quote parsing errors.
    """
    input_len = len(input)
    argv = list[str]()

    arg_idx = start_idx
    while arg_idx < input_len:
        arg_idx = _traverse_spaces(input, arg_idx)

        # Stop if the end was reached.
        if arg_idx == input_len:
            break
        arg, arg_idx = _traverse_arg(input, arg_idx)
        
        if arg_idx != input_len and input[arg_idx] != SPACE:
            raise SpaceError("Arguments must be separated by space.")
        argv.append(arg)
    return argv

def parser(input: str) -> tuple[str, list[str]]:
    """
    Parses the input string into a list of tokens.

    Parameters:
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
    if input_len < 3:
        raise ValueError("The input string must contain at least one (supported) command.")
    
    # Skip first idx spaces.
    idx = 0
    while idx < input_len and input[idx] == SPACE:
        idx += 1
    
    space_idx = input.find(SPACE, idx)
    
    # Assume that there is only one token - the command.
    # str.find() returns -1 if the substring is not found.
    # The command is updated if a white space was found.
    if space_idx == NOT_FOUND_INDEX:
        return input[idx:input_len], []
    
    cmd = input[idx:space_idx]

    # space_idx + 1 == next position of a potential non-white-space char.
    argv = _get_argv(input, space_idx + 1)
    return cmd, argv

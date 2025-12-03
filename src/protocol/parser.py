from .constants_resp import SPACE

def _get_argv(input: str, start_idx: int) -> list[str]:
    """
    Internal method.
    Extract command arguments from an input string.

    This function parses the substring of `input` beginning at `start_idx`,
    splitting it on space characters and returning the resulting tokens.
    Consecutive characters are ignored.

    Parameters:
        input (str): The full input string containing a command and its arguments.
        start_idx (int): The index in `input` from which argument parsing should begin.

    Returns:
        list[str]: A list of argument strings. If no spaces are found after `start_idx`, it's empty.
    """
    input_len = len(input)
    argv = list[str]()

    prev_arg_idx = start_idx
    for idx in range(start_idx, input_len):
        if input[idx] != SPACE:
            continue
        # Found space.
        if idx != prev_arg_idx:
            argv.append(input[prev_arg_idx:idx])
        prev_arg_idx = idx + 1

    # The input did not end with an space.
    if prev_arg_idx != input_len:
        argv.append(input[prev_arg_idx:input_len])
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
    """
    input_len = len(input)

    # All commands have a length greater of equal to 3.
    if input_len < 3:
        raise ValueError("The input string must contain at least one command.")
    
    space_idx = input.find(" ")
    
    # Assume that there is only one token - the command.
    # str.find() returns -1 if the substring is not found.
    # The command is updated if a white space was found.
    cmd = input
    if space_idx != -1:
        cmd = input[0:space_idx]

    # space_idx + 1 == next position of a potential non-white-space char.
    argv = _get_argv(input, space_idx + 1)
    return cmd, argv

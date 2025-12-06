from .constants_cmds import CMD_DS_MAP, CONNECTION_CMDS, GENERIC_CMDS
from .exceptions import ArgumentCountError

def needs_ds_check(cmd: str) -> bool:
    """
    If the current command is specific to a Redis data structure, then the given argument(s) must be of that specific data structure. Therefore more validation will be required.

    Returns:
        bool: If extra validation step is required.
    """
    try:
        CMD_DS_MAP[cmd]
        return True
    except:
        return False

def _validate_ds(cmd: str):
    data_structure = None
    if needs_ds_check(cmd):
        data_structure = CMD_DS_MAP[cmd]
    # todo data_structure validation

def _validate_len():
    pass

def _validate_arg(arg: str):
    """
    Ensures that the argument value is valid.
    """
    pass

def sanitizer(cmd: str, argv: list[str]) -> None:
    """
    Performs these **input** validations:

    0. tests if the command is valid/supported and under 512MB
    1. verifies that the number of arguments falls within the allowed range for the command
    2. if the command targets a specific Redis data structure, checks that the argument(s) match the expected type(s)

    The actual argument sanitization is performed in `arg_sanitizer()`.

    Raises:
        KeyError: If the command is invalid.
        ArgumentCountError: If the input arguments for an command are either missing or too many.
    """
    argc = len(argv)
    if cmd in CONNECTION_CMDS:
        if argc != 0:
            raise ArgumentCountError("Connection commands do not accept arguments.")
        return

    if cmd in GENERIC_CMDS:
        # todo check for each the amount of arguments it accepts.
        return

    # If the command is either not supported or invalid, this will throw.
    data_structure = CMD_DS_MAP[cmd]
    # todo check for each the amount of arguments it accepts.
    
    raise KeyError("Command is either not supported or not existent.")

def arg_sanitizer(arg: str) -> None:
    """
    Validates arguments.
    This should be called **only** by the encoder module.
    

    o be done in encoder and under 512MB
    """
    pass

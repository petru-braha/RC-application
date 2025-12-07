from frozendict import frozendict
from .constants_cmds import CmdDef, CONNECTION_CMDS, CMDS
from .exceptions import ArgumentCountError

def _count_opt(argv: list[str], cmd_def: CmdDef) -> int:
    """
    Counts how many optional command options appear in the provided argument list.

    Parameters:
        cmd_def (CmdDef): The command definition object containing optional options
                          in its `opt` attribute.

    Returns:
        int: The number of optional option keywords found in `argv`.
    """
    if cmd_def.opt == None:
        return 0
    
    optc = 0
    # Here arg stands for input argument.
    for arg in argv:
        # cmd_def.opt here is a list of dicts.
        for opt in cmd_def.opt:
            if arg in opt:
                optc += opt[arg] + 1
    return optc

def _validate_argc(cmd: str, argv: list[str], cmd_dict: frozendict[str, CmdDef]) -> None:
    """
    Validates that the number of arguments provided for a Redis command
    meets the minimum required count, ignoring optional arguments.

    Parameters:
        cmd (str): The Redis command name.
        argv (arr): List of arguments provided for the command.
        cmd_dict: Mapping of command names to RedisCommand objects, used to
             retrieve metadata about required and optional arguments.

    Raises:
        ArgumentCountError: If the number of arguments (excluding optional options)
                            is less than the required minimum for the command.
    """
    argc = len(argv)
    cmd_def = cmd_dict[cmd]
    
    # Options count.
    optc = _count_opt(argv, cmd_def)
    # Options are not required.
    # Their count shouldn't make up for the missing required arguments.
    argc -= optc
    if argc < cmd_def.required_argc:
        raise ArgumentCountError("Missing required arguments: only {argc} provided.")

    # todo check pair count
    # todo check required after pairs count

def sanitizer(cmd: str, argv: list[str]) -> None:
    """
    Performs these **input** validations:

    0. tests if the command is valid
    1. verifies that the number of arguments falls within the allowed range for the command
    2. if the command targets a specific Redis data structure, checks that the argument(s) match the expected type(s)

    The actual argument sanitization is performed in `arg_sanitizer()`.

    Raises:
        KeyError: If the command is invalid.
        ArgumentCountError: If the input arguments for an command are either missing or too many.
    """
    argc = len(argv)
    for cmd_dict in CMDS:
        if cmd not in cmd_dict:
            continue
        _validate_argc(cmd, argv, cmd_dict)
        break
    raise KeyError("Command is either not supported or not existent.")

from frozendict import frozendict
from .cmds import *
from .exceptions import ArgumentCountError

def _validate_int(arg: str) -> None:
    try:
        int(arg)
    except:
        raise TypeError("")

def _validate_flt(arg) -> int:
    pass
def _validate_str(arg) -> int:
    pass
def _validate_args(arg_def, arg_input) -> int:
    pass
def _validate_opts(arg_def, arg_input) -> int:
    pass
def _validate_opt_set(arg_def, arg_input) -> int:
    pass

def _validate_arg(arg_def: Arg, argv: list[str], arg_idx):
    if isinstance(arg_def, IntArg):
        _validate_int(argv[arg_idx])
        return arg_idx + 1
    if isinstance(arg_def, FltArg):
        pass
    if isinstance(arg_def, StrArg):
        pass
    if isinstance(arg_def, Args):
        pass
    if isinstance(arg_def, Opts):
        pass
    if isinstance(arg_def, OptSet):
        pass

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
    cmd_dict = None
    for cmd_dict in CMDS:
        if cmd not in cmd_dict:
            continue
        cmd_dict = cmd_dict
        break
    
    if cmd_dict == None:
        raise KeyError("Command is either not supported or not existent.")

    cmd_args_def = cmd_dict[cmd]
    arg_idx = 0
    for arg_section in cmd_args_def:
        arg_idx = _validate_arg(arg_section, argv, arg_idx)


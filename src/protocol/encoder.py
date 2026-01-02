from .constants_resp import RespDataType, RESP_SYMB, CRLF

def _encode_arg(arg: str) -> str:
    """
    Internal method.
    Encodes an argument as a bulk string.
    """
    encoded = RESP_SYMB[RespDataType.BULK_STRINGS] + str(len(arg)) + CRLF
    encoded += (arg + CRLF)
    return encoded

def encoder(cmd: str, argv: list[str]) -> str:
    """
    Encodes the cmd and the arguments.
    Must be used after running the sanitizer.

    Parameters:
        cmd (str): The command string (e.g. "GET").
        argv (list[str]): The argument values for the command.

    Returns:
        str: The entire encoded command and arguments,
             all following the RESP Config.
    """
    argc = len(argv)
    # argc + 1 is necessary since we also send the command itself.
    encoded = RESP_SYMB[RespDataType.ARRAYS] + str(argc + 1) + CRLF
    encoded += _encode_arg(cmd)
    for idx in range(argc):
        encoded += _encode_arg(argv[idx])
    return encoded

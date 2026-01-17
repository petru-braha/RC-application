import core

from network import Connection, Receiver
from protocol import parser, encoder, decoder, Output, OutputErr, ParserError

from .exceptions import Resp3NotSupportedError

logger = core.get_logger(__name__)

def process_input(input_str: str) -> bytes:
    """
    Processes the input string by parsing it into a command and arguments,
    encoding it, and returning the encoded bytes.
    
    Args:
        input_str (str): A string representing the input to be processed.
    
    Returns:
        bytes: The encoded bytes of the input string.

    Raises:
        ValueError: If the input string is invalid.
    """
    logger.debug(f"Processing input: {input_str}.")
    
    try:
        cmd, argv = parser(input_str)
    except (ValueError, ParserError) as e:
        raise ValueError(f"Invalid input {input_str}; {e}")
    logger.debug(f"Parsed command: {cmd}, arguments: {argv}.")
    
    # todo sanitizer
    
    encoded = encoder(cmd, argv)
    return encoded.encode(core.ASCII_ENC)

def process_output(receiver: Receiver) -> str:
    """
    Processes the output string by decoding it and formatting it.
    
    Args:
        receiver (Receiver): The receiver to process.
    
    Returns:
        obj: The processed output object.

    Raises:
        PartialResponseError: If the buffer provided by receiver is incomplete.
        AssertionError: If the output type is NOT one of the expected Output subclasses.
    """
    logger.debug("Processing output.")

    try:
        return decoder(receiver)
    
    except core.PartialResponseError as e:
        logger.debug(f"Partial output received: {e}.")
        raise
    
    except Exception as e:
        logger.error(f"Error when decoding output: {e}.", exc_info=True)
        raise

def is_init_command(cmd: str) -> bool:
    """
    Checks if the command ran at the connection initialization (HELLO and SELECT).
    
    Args:
        cmd (str): The raw command string given as input.
    """
    return Connection.SELECT_CMD in cmd or Connection.HELLO_CMD in cmd

def validate_init_cmd_output(cmd: str, output: Output) -> None:
    """
    Checks if the command ran at the connection initialization (HELLO and SELECT).
    If so checks if they returned an error.
    
    If HELLO RESP3 failed, retries it with RESP2 protocol version.
    If SELECT failed, notify the client .
    
    Args:
        cmd (str): The raw command string given as input.
        output (obj): The output object.

    Raises:
        Resp3NotSupportedError: If the third protocol version is not supported by the remote instance.
        ValueError: If the command is not responsible for the initialization of the connection.
    """
    logger.debug(f"Processing transmission: {cmd} -> {output}.")

    if Connection.SELECT_CMD in cmd:
        if not isinstance(output, OutputErr):
            logger.info("Connection initialization on a specific database instance (SELECT command) successful.")
            return
        
        logger.error(f"Connection initialization on a specific database instance (SELECT command) failed: {output.value}.")
        return
    
    if Connection.HELLO_CMD not in cmd:
        return
    
    if not isinstance(output, OutputErr):
        logger.info("HELLO command successful.")
        return
    
    logger.error(f"HELLO command failed: {output.value}.")
    # Check if `HELLO 3` and `HELLO 2` both failed.
    # If so, there is nothing else to do.
    if f"{Connection.HELLO_CMD} {core.RespVer.RESP2}" in cmd:
        logger.error("HELLO command failed with RESP2 protocol version.")
        logger.info("The user should try authentication with AUTH command.")
    
    # Only `HELLO 3` failed, so retry with RESP2.
    if f"{Connection.HELLO_CMD} {core.RespVer.RESP3}" in cmd:
        raise Resp3NotSupportedError("Invalid protocol version: 3")

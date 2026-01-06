from core.config import get_logger
from core.constants import ASCII_ENC
from core.exceptions import PartialResponseError

from network import Connection, Receiver
from protocol import parser, encoder, decoder, Output, OutputErr, ParserError

logger = get_logger(__name__)

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
    return encoded.encode(ASCII_ENC)

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
    logger.debug(f"Processing output.")

    try:
        output = decoder(receiver)
        logger.debug(f"Decoded output: {output}.")
        return output
    
    except PartialResponseError as e:
        logger.debug(f"Partial output received: {e}.")
        raise
    
    except Exception as e:
        logger.error(f"Error when decoding output: {e}.", exc_info=True)
        raise

def process_transmission(connection: Connection, raw_input: str, output: Output) -> None:
    """
    Checks if the input was responsible for the initialization of the connection (HELLO and SELECT).
    If so checks if they returned an error.
    
    If HELLO RESP3 failed, retries it with RESP2 protocol version.
    If SELECT failed, notify the client .
    
    Args:
        connection (obj): The connection object.
        raw_input (str): The raw input string.
        output (obj): The output output.
    """
    logger.debug(f"Processing transmission: {raw_input} -> {output}.")

    if Connection.SELECT_CMD in raw_input:
        if not isinstance(output, OutputErr):
            logger.info("Connection initialization on a specific database instance (SELECT command) successful.")
            return
        
        logger.error(f"Connection initialization on a specific database instance (SELECT command) failed: {output.value}.")
        return
    
    if Connection.HELLO_CMD not in raw_input:
        return
    
    if not isinstance(output, OutputErr):
        logger.info("HELLO command successful.")
        return
    
    logger.error(f"HELLO command failed: {output.value}.")
    # Check if we should retry with RESP2.
    # Only retry if we were trying RESP3 and it wasn't a manual retry.
    if Connection.RESP3 in raw_input:
        logger.info("Retrying with RESP2...")
        connection.say_hello(connection.initial_user, 
                             connection.initial_pasw, 
                             Connection.RESP2)
    elif Connection.RESP2 in raw_input:
        logger.error("HELLO command failed with RESP2 protocol version.")
        logger.info("The user should try authentication with AUTH command.")

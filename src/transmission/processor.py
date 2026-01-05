from core.config import get_logger
from core.constants import ASCII_ENC
from core.exceptions import PartialResponseError

from network import Connection, Receiver
from protocol import parser, encoder, decoder, formatter
from protocol import ParserError

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
    logger.debug(f"Encoded command: {encoded}.")
    
    return encoded.encode(ASCII_ENC)

def process_output(receiver: Receiver) -> str:
    """
    Processes the output string by decoding it and formatting it.
    
    Args:
        receiver (Receiver): The receiver to process.
    
    Returns:
        str: The processed output string.

    Raises:
        PartialResponseError: If the buffer provided by receiver is incomplete.
        AssertionError: If the output type is NOT one of the expected Output subclasses.
    """
    logger.debug(f"Processing output for {str(receiver.addr)}.")

    try:
        output = decoder(receiver)
        formatted = formatter(output)
        
        logger.debug(f"Formatted output: {formatted}.")
        return formatted
    
    except PartialResponseError as e:
        logger.debug(f"Partial output received: {e}.")
        raise
    
    except Exception as e:
        logger.error(f"Error when processing data from {receiver.addr}: {e}.", exc_info=True)
        raise

def process_transmission(connection: Connection, raw_input: str, output: str) -> None:
    """
    Checks if the input was responsible for the initialization of the connection (HELLO and SELECT).
    If so checks if they returned an error.
    
    If HELLO RESP3 failed, retries it with RESP2 protocol version.
    If SELECT failed, notify the client .
    
    Args:
        connection (obj): The connection object.
        raw_input (str): The raw input string.
        output (str): The output string.
    """
    logger.debug(f"Processing transmission: {raw_input} -> {output}.")

    # todo
    if Connection.SELECT_CMD in raw_input:
        # if output error
        logger.error("SELECT command failed.")
        # if output success
        logger.info("SELECT command successful.")
        return
    
    if Connection.HELLO_CMD in raw_input:
        # if output error
        logger.error("HELLO command failed.")
        # if output success
        logger.info("HELLO command successful.")
        connection.say_hello()
        return

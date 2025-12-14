from frozendict import frozendict
from typing import Callable

from src.constants import NOT_FOUND_INDEX

from .constants_resp import RespDataType, \
                            SYMB_TYPE, NULL_LENGTH, \
                            CRLF, NULL
from .output import Output, OutputStr, OutputSeq, OutputMap, OutputAtt

class _Decoder:
    """
    Internal helper class.

    Decodes Redis RESP3/RESP2-encoded strings into structured Output objects,
    preserving the original hierarchical structure.

    Attributes:
        output (str): The raw RESP3 string to decode.
        output_idx (int): The current index during traversal.
        decoded (Output): The fully decoded representation of the input.
    """

    # Static dispatcher mapping RESP data types to traversal methods.
    # This is a class-level field shared by all instances;
    # It is initialized exactly once after the class is defined.
    _TRAVERSERS: frozendict[RespDataType, Callable]
    """
    Internal dispatcher.

    Maps RESP3 data types to their traversal functions.

    Used by `_traverser()` to decode values based on type.
    Each function returns `(decoded_string, next_index)`.
    """
    
    def __init__(self, output: str) -> None:
        self._output = output
        self._output_idx = 0
        self.decoded = self._traverser()

    def _traverser(self) -> Output:
        """
        Internal method.

        Dispatches traversal logic based on the RESP data type prefix symbol.

        Raises:
            KeyError: Invalid first byte of an output.
        """
        symb = self._output[self._output_idx]

        # idx always points to the not read character.
        self._output_idx += 1
        data_type = SYMB_TYPE[symb]

        # Call the appropriate method for the first byte received.
        traverser = _Decoder._TRAVERSERS[data_type]
        return traverser(self)

    def _traverse_crlf(self) -> OutputStr:
        """
        Internal method.

        Handles simple strings, simple errors, RESP null values, and similar types.

        Traverses the Redis output from `start_idx` until the CRLF terminator.
        
        Example: Input "+OK\r\n" returns OutputStr("OK").

        Raises:
            ValueError: the output received is invalid and not ended by CRLF.
        """
        end_idx = self._output.find(CRLF, self._output_idx)
        if end_idx == NOT_FOUND_INDEX:
            raise ValueError("Invalid Redis response.", self._output)
        
        output = OutputStr(self._output[self._output_idx:end_idx])
        self._output_idx = end_idx + len(CRLF)
        return output

    def _traverse_null(self) -> OutputStr:
        """
        Internal method.

        Parses a RESP null value.

        Returns the constant `NULL` and the index after the CRLF.
        
        Example: Input "_\r\n" returns OutputStr("NULL").
        """
        self._traverse_crlf()
        return OutputStr(NULL)
    
    def _traverse_bulk_string(self) -> OutputStr:
        """
        Internal method.

        Parses a bulk string by first reading its declared length,
        followed by the string content itself.
        
        Example: Input "$6\r\nfoobar\r\n" returns OutputStr("foobar").
        """
        length_str = self._traverse_crlf().value
        length = int(length_str)

        if length == NULL_LENGTH:
            return OutputStr(NULL)

        value = self._output[self._output_idx:self._output_idx + length]
        self._output_idx += length + len(CRLF)
        return OutputStr(value)

    def _traverse_bulk_error(self) -> OutputStr:
        """
        Internal method.

        Similar to the bulk string traverser.
        
        Example: Input "!5\r\nError\r\n" returns OutputStr("Error").
        """
        _ = self._traverse_crlf()
        return self._traverse_crlf()

    def _traverse_verbatim_string(self) -> OutputStr:
        """
        Internal method.

        Parses a verbatim string, which consists of:
        - Three bytes specifying the encoding
        - A colon separator
        - The string data
        
        Example: Input "=9\r\ntxt:Hello\r\n" returns OutputStr("Hello").
        """
        _ = self._traverse_crlf()
        value = self._traverse_crlf().value
        # 4 bytes are skipped: enconding bytes and the ":" character.
        return OutputStr(value[4:])
    
    def _traverse_sequence(self) -> OutputSeq:
        """
        Internal method.

        Parses aggregate RESP types such as arrays, sets, and pushes.
        Although this client does not use commands that emit push messages,
        the decoder can still interpret them.
        
        Example: Input "*2\r\n:1\r\n:2\r\n" returns OutputSeq((OutputStr("1"), OutputStr("2"))).
        """
        length = int(self._traverse_crlf().value)
        elements = tuple(self._traverser() for _ in range(length))
        return OutputSeq(elements)

    def _traverse_map(self) -> OutputMap:
        """
        Internal method.

        Parses aggregate key-value structures such as RESP maps and attributes.
        
        Example: Input "%1\r\n+k\r\n+v\r\n" returns OutputMap({OutputStr("k"): OutputStr("v")}).
        """
        length = int(self._traverse_crlf().value)
        result = {}
        for _ in range(length):
            key = self._traverser()
            val = self._traverser()
            result[key] = val
        result = frozendict(result)
        return OutputMap(result)
    
    def _traverse_attribute(self) -> OutputAtt:
        """
        Internal method.

        Parses a attributes and message. This consists of:
        - a key-value map (the attributes)
        - the actual data payload following the map
        
        Example: Input "|1\r\n+k\r\n+v\r\n:1\r\n" returns
                 OutputAtt({OutputStr("k"): OutputStr("v")}, OutputStr("1")).
        """
        attributes = self._traverse_map()
        output = self._traverser()
        return OutputAtt(attributes, output)

_Decoder._TRAVERSERS = frozendict({
    RespDataType.SIMPLE_STRINGS: _Decoder._traverse_crlf,
    RespDataType.SIMPLE_ERRORS: _Decoder._traverse_crlf,
    RespDataType.INTEGERS: _Decoder._traverse_crlf,
    RespDataType.BULK_STRINGS: _Decoder._traverse_bulk_string,
    RespDataType.ARRAYS: _Decoder._traverse_sequence,
    RespDataType.NULLS: _Decoder._traverse_null,
    RespDataType.BOOLEANS: _Decoder._traverse_crlf,
    RespDataType.DOUBLES: _Decoder._traverse_crlf,
    RespDataType.BIG_NUMBERS: _Decoder._traverse_crlf,
    RespDataType.BULK_ERRORS: _Decoder._traverse_bulk_error,
    RespDataType.VERBATIM_STRINGS: _Decoder._traverse_verbatim_string,
    RespDataType.MAPS: _Decoder._traverse_map,
    RespDataType.ATTRIBUTES: _Decoder._traverse_attribute,
    RespDataType.SETS: _Decoder._traverse_sequence,
    RespDataType.PUSHES: _Decoder._traverse_sequence,
})

def decoder(output: str) -> Output:
    """
    Decodes a RESP-encoded Redis response.

    The input is assumed to be well-formed according to RESP rules.

    Parameters:
        output (str): The raw RESP-encoded (Redis) response string.

    Returns:
        str: The decoded value, represented as a string.

    Raises:
        RuntimeError: Unexpected exceptions.
    """
    try:
        decoder = _Decoder(output)
        return decoder.decoded
    except BaseException as e:
        raise RuntimeError("Decoder failure.") from e

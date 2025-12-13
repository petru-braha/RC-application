from frozendict import frozendict

from src.constants import NOT_FOUND_INDEX

from .constants_resp import RespDataType, \
                            SYMB_TYPE, NULL_LENGTH, \
                            CRLF, NULL
from .output import Output, OutputStr, OutputSeq, OutputMap, OutputAtt

class _Decoder:
    """
    Decodes Redis RESP3/RESP2-encoded strings into structured Output objects,
    preserving the original hierarchical structure.

    Attributes:
        output (str): The raw RESP3 string to decode.
        output_idx (int): The current index during traversal.
        decoded (Output): The fully decoded representation of the input.
    """
    
    def __init__(self, output: str) -> None:
        self._TRAVERSERS = frozendict({
            RespDataType.SIMPLE_STRINGS: self._traverse_crlf,
            RespDataType.SIMPLE_ERRORS: self._traverse_crlf,
            RespDataType.INTEGERS: self._traverse_crlf,
            RespDataType.BULK_STRINGS: self._traverse_bulk_string,
            RespDataType.ARRAYS: self._traverse_sequence,
            RespDataType.NULLS: self._traverse_null,
            RespDataType.BOOLEANS: self._traverse_crlf,
            RespDataType.DOUBLES: self._traverse_crlf,
            RespDataType.BIG_NUMBERS: self._traverse_crlf,
            RespDataType.BULK_ERRORS: self._traverse_bulk_error,
            RespDataType.VERBATIM_STRINGS: self._traverse_verbatim_string,
            RespDataType.MAPS: self._traverse_map,
            RespDataType.ATTRIBUTES: self._traverse_attribute,
            RespDataType.SETS: self._traverse_sequence,
            RespDataType.PUSHES: self._traverse_sequence,
        })
        """
        Internal dispatcher.

        Maps RESP3 data types to their traversal functions.

        Used by `_traverser()` to decode values based on type.
        Each function returns `(decoded_string, next_index)`.
        """
        self.output = output
        self.output_idx = 0
        self.decoded = self._traverser()

    def _traverser(self) -> Output:
        """
        Internal method.

        Dispatches traversal logic based on the RESP data type prefix symbol.

        Raises:
            KeyError: Invalid first byte of an output.
        """
        symb = self.output[self.output_idx]

        # idx always points to the not read character.
        self.output_idx += 1
        data_type = SYMB_TYPE[symb]

        # Call the appropriate method for the first byte received.
        return self._TRAVERSERS[data_type]()

    def _traverse_crlf(self) -> OutputStr:
        """
        Internal method.

        Handles simple strings, simple errors, RESP null values, and similar types.

        Traverses the Redis output from `start_idx` until the CRLF terminator.

        Raises:
            ValueError: the output received is invalid and not ended by CRLF.
        """
        end_idx = self.output.find(CRLF, self.output_idx)
        if end_idx == NOT_FOUND_INDEX:
            raise ValueError("Invalid Redis response.", self.output)
        
        output = OutputStr(self.output[self.output_idx:end_idx])
        self.output_idx = end_idx + len(CRLF)
        return output

    def _traverse_null(self) -> OutputStr:
        """
        Internal method.

        Parses a RESP null value.

        Returns the constant `NULL` and the index after the CRLF.
        """
        self._traverse_crlf()
        return OutputStr(NULL)
    
    def _traverse_bulk_string(self) -> OutputStr:
        """
        Internal method.

        Parses a bulk string by first reading its declared length,
        followed by the string content itself.
        """
        length_str = self._traverse_crlf().value
        length = int(length_str)

        if length == NULL_LENGTH:
            return OutputStr(NULL)

        value = self.output[self.output_idx:self.output_idx + length]
        self.output_idx += length + len(CRLF)
        return OutputStr(value)

    def _traverse_bulk_error(self) -> OutputStr:
        """
        Internal method.

        Similar to the bulk string traverser.
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
        """
        length = int(self._traverse_crlf().value)
        elements = tuple(self._traverser() for _ in range(length))
        return OutputSeq(elements)

    def _traverse_map(self) -> OutputMap:
        """
        Internal method.

        Parses aggregate key-value structures such as RESP maps and attributes.
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
        """
        attributes = self._traverse_map()
        output = self._traverser()
        return OutputAtt(attributes, output)

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

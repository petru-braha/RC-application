from frozendict import frozendict
from typing import Callable

from core.config import Config
from core.constants import STR_TRAVERSAL_STRIDE, CRLF
from network import Receiver

from .constants_resp import RespDataType, \
                            SYMB_TYPE, NULL_LENGTH, \
                            NULL
from .output import Output, OutputStr, OutputSeq, OutputMap, OutputAtt

logger = Config.get_logger(__name__)

def decoder(receiver: Receiver) -> Output:
    """
    Decodes a RESP-encoded Redis response using a Receiver instance.

    The input is assumed to be well-formed according to RESP rules.

    Parameters:
        receiver (obj): The receiver instance to consume data from.

    Returns:
        Output: The decoded value.

    Raises:
        PartialResponseError: If the buffer provided by receiver is incomplete.
        ConnectionError: If the connection is closed during reading.
    """
    decoder = _Decoder(receiver)
    return decoder.decoded

class _Decoder:
    """
    Internal helper class.

    Decodes Redis RESP3/RESP2-encoded strings into structured Output objects,
    preserving the original hierarchical structure.

    Attributes:
        receiver (Receiver): The receiver source.
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
    """
    
    _COLON_SEP: str = ":"
    """
    Internal constant.

    The separator between the encoding and the content in a verbatim string.
    """
    
    def __init__(self, receiver: Receiver) -> None:
        self._receiver = receiver
        self.decoded = self._traverser()

    def _traverser(self) -> Output:
        """
        Internal method.

        Dispatches traversal logic based on the RESP data type prefix symbol.

        Raises:
            KeyError: Invalid first byte of an output.
            PartialResponseError: If the buffer is empty.
        """
        symb = self._receiver.consume(STR_TRAVERSAL_STRIDE)
        try:
            data_type = SYMB_TYPE[symb]
        except KeyError:
            logger.error(f"Unknown RESP type byte received: {symb!r}")
            raise

        # Call the appropriate method for the first byte received.
        traverser = _Decoder._TRAVERSERS[data_type]
        return traverser(self)

    def _traverse_crlf(self) -> OutputStr:
        """
        Internal method.

        Handles simple strings, simple errors, RESP null values, and similar types.

        Traverses the Redis output until the CRLF terminator.
        
        Example: Input "+OK\r\n" returns OutputStr("OK").

        Raises:
            PartialResponseError: If CRLF is missing.
        """
        line = self._receiver.consume_crlf()
        return OutputStr(line)

    def _traverse_null(self) -> OutputStr:
        """
        Internal method.

        Parses a RESP null value.

        Returns the constant `NULL`.
        
        Example: Input "_\r\n" returns OutputStr("NULL").
        """
        self._traverse_crlf()
        return OutputStr(NULL)
    
    def _traverse_bulk(self) -> OutputStr:
        """
        Internal method.

        Parses a bulk types by reading its declared length,
        followed by the content itself.
        
        Example: Input "$6\r\nfoobar\r\n" returns OutputStr("foobar").
        """
        length_str = self._traverse_crlf().value
        length = int(length_str)

        if length == NULL_LENGTH:
            return OutputStr(NULL)

        value = self._receiver.consume(length)
        self._receiver.consume(len(CRLF))
        return OutputStr(value)

    def _traverse_verbatim(self) -> OutputStr:
        """
        Internal method.

        Parses a verbatim string, which consists of:
        - Three bytes specifying the encoding
        - A colon separator
        - The string data
        
        Example: Input "=9\r\ntxt:Hello\r\n" returns OutputStr("Hello").
        """
        content = self._traverse_bulk().value
        # Under the assumption that the server sends valid verbatim strings,
        # we can safely assume that the index method does not raise errors.
        start_idx = content.index(_Decoder._COLON_SEP)
        return OutputStr(content[start_idx + len(_Decoder._COLON_SEP) : ])
    
    def _traverse_sequence(self) -> OutputSeq:
        """
        Internal method.

        Parses aggregate RESP types such as arrays, sets, and pushes.
        Although RC-application does not support push messages,
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
    RespDataType.BULK_STRINGS: _Decoder._traverse_bulk,
    RespDataType.ARRAYS: _Decoder._traverse_sequence,
    RespDataType.NULLS: _Decoder._traverse_null,
    RespDataType.BOOLEANS: _Decoder._traverse_crlf,
    RespDataType.DOUBLES: _Decoder._traverse_crlf,
    RespDataType.BIG_NUMBERS: _Decoder._traverse_crlf,
    RespDataType.BULK_ERRORS: _Decoder._traverse_bulk,
    RespDataType.VERBATIM_STRINGS: _Decoder._traverse_verbatim,
    RespDataType.MAPS: _Decoder._traverse_map,
    RespDataType.ATTRIBUTES: _Decoder._traverse_attribute,
    RespDataType.SETS: _Decoder._traverse_sequence,
    RespDataType.PUSHES: _Decoder._traverse_sequence,
})

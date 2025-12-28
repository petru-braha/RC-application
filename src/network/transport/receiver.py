from structs import Address
from exceptions import PartialResponseError

from .sock import Sock
from protocol.constants_resp import CRLF

class Receiver(Sock):
    _4KB_BUFSIZE: int = 4096

    def __init__(self, addr: Address) -> None:
        super().__init__(addr)
        self._buf = bytearray()

    def consume(self, bufsize: int) -> str:
        if bufsize > len(self._buf):
            raise PartialResponseError(f"Insufficient buffer bytes: {len(self._buf)}. Needed: {bufsize}")
        
        data = self._buf[:bufsize]
        del self._buf[:bufsize]
        return data.decode()

    def consume_crlf(self) -> str:
        sep = CRLF.encode()
        try:
            idx = self._buf.index(sep)
        except ValueError:
            raise PartialResponseError("Buffer does not contain a CRLF.")
        
        end_pos = idx + len(sep)
        data = self._buf[:end_pos]
        del self._buf[:end_pos]
        return data.decode()

    def recv(self) -> int:
        try:
            data = super().recv(self._4KB_BUFSIZE) # calls socket.recv
            if not data:
                return 0
            self._buf.extend(data)
            return len(data)
        except BlockingIOError:
            return 0
        except OSError:
            return 0
            
    def has_leftovers(self) -> bool:
        return len(self._buf) > 0
    
    def empty_buf(self) -> bool:
        return len(self._buf) == 0

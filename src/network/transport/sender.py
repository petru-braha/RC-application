from collections import deque

from structs import Address

from .sock import Sock

class Sender(Sock):
    
    def __init__(self, addr: Address) -> None:
        super().__init__(addr)
        self._pending_cmds = deque()

    def append_cmd(self, cmd: str):
        self._pending_cmds.append(cmd)

    def has_pending_cmds(self) -> bool:
        return len(self._pending_cmds) > 0

    def get_pending_cmd(self) -> str | None:
        if not self._pending_cmds:
            return None
        return self._pending_cmds[0]

    def remove_pending_cmd(self):
        if self._pending_cmds:
            self._pending_cmds.popleft()

    def send_data(self, data: bytes):
        try:
            self.sendall(data)
        except OSError:
            pass
            # todo

from collections import deque

from src.network import Sock
    
class Sender:

        # todo send hello, send select
    _sock_cmds: dict[Sock, deque[str]]

    @staticmethod
    def register(sock: Sock):
        Sender._sock_cmds[sock] = deque()

    @staticmethod
    def unregister(sock: Sock):
        Sender._sock_cmds.pop(sock, None)

    @staticmethod
    def append_cmd(sock: Sock, cmd: str):
        Sender._sock_cmds[sock].append(cmd)

    @staticmethod
    def send(sock: Sock, encoded: str):
        """
        simple Connection.
        Actually called by
        """
        dialogue = Dialogue(encoded, None)
        _AppState.get_history[connection].append(dialogue)

    @staticmethod
    def handle_write(connection: Connection) -> bool:
        hist = AppState.sock_hist_dict[connection]

        for dialogue in hist:
            if dialogue.output == None:
                bytes = prepare_cmd(dialogue.cmd)
                connection.sendall(bytes)
                return True
        return False

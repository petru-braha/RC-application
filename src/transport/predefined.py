# from src.protocol.cmds import AUTH_ARG
# from src.output import OutputStr, OutputMap
# 
# 
# _SELECT_CMD: str = "SELECT"
#     """
#     The Redis command used to chose the database logical segment.
#     """
# 
#     _ERR_STR: str = "ERR"
#     """
#     Select command error message prefix.
#     """
#         if db_idx != None and db_idx != Connecter._DEFAULT_DB:
#             self._say_select(db_idx)
# 
#     def _say_select(self, db_idx: int) -> None:
#         """
#         """
#         argv = [str(db_idx)]
#         msg = join_cmd_argv(Connecter._SELECT_CMD, argv)
#         output = self.send(msg)
#         
#         assert isinstance(output, OutputStr)
#         output = output.value
#         if Connecter._ERR_STR in output:
#             raise ConnectionError(output)
#         
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
#     _HELLO_CMD: str = "HELLO"
#     """
#     The Redis command used to negotiate protocol version and authenticate.
#     """
#     _RESP2: str = "2"
#     """
#     RESP version 2 identifier.
#     """
#     _RESP3: str = "3"
#     """
#     RESP version 3 identifier.
#     """
# 
#     _ERR_NOPROTO: str = "NOPROTO"
#     """
#     """
#     _ERR_UNKNOWN: str = "unknown command"
#     """
#     """
# 
# 
# 
#         # There is no default password.
#         self._say_hello(user, pasw)
# 
#     def _say_hello(self, user: str, pasw: str | None, protver: str = _RESP3) -> None:
#         """
#         Performs the initial handshake with the Redis server.
# 
#         Negotiates the protocol version (RESP3 by default) and authenticates 
#         the user if credentials are provided. If the server does not support 
#         RESP3, it automatically falls back to RESP2.
# 
#         Args:
#             user: The username for ACL authentication (use EMPTY_STR for default).
#             pasw: The password for authentication.
#             protver: The protocol version to attempt (default is "3").
# 
#         Raises:
#             ConnecterError: If authentication fails or a protocol error occurs 
#                             that isn't related to versioning.
#         """
#         argv = [protver]
#         if user != Identificator._DEFAULT_USER and pasw != None:
#             argv.extend([AUTH_ARG.pattern, user, pasw])
#         msg = join_cmd_argv(Identificator._HELLO_CMD, argv)
#         
#         self.send(msg)
# 
#     def connected(self) -> bool:
#         """
#         Non-blocking check if the handshake is complete.
#         
#         Returns:
#             bool: True if the handshake was completed.
#         """
#         if self._was_hello_recv():
#             return True
# 
#         # Check the last dialog to see if it was a failed HELLO or needs fallback.
#         if not self.history:
#             return False
#             
#         dialog = self.history[-1]
#         
#         # If the last command was NOT HELLO, we can't do much here about handshake logic 
#         # unless we strictly assume handshake is the first thing.
#         if Identificator._HELLO_CMD not in dialog.cmd:
#              # Should practically not happen if we only queue HELLO first.
#              return False
# 
#         if isinstance(dialog.output_node, OutputMap):
#             return True
#         
#         # Handle failure/fallback cases based on the last response.
#         output = dialog.output
#         is_unsupported = any(msg in output
#                            for msg in [
#                                Identificator._ERR_NOPROTO,
#                                Identificator._ERR_UNKNOWN])
#                                
#         # Assuming we track which version we tried last? 
#         # For simplicity, if we see a failure for RESP3, we try RESP2.
#         # But we need to know what we just sent.
#         # Let's inspect the command payload or just infer from history length?
#         # If history has 1 item and it failed, it was RESP3.
#         
#         if len(self.history) == 1 and is_unsupported:
#              # We tried RESP3 (default) and it failed. Fallback to RESP2.
#              # We need to re-send HELLO with version 2.
#              # This sends it into the write queue.
#              # But we need to make sure we don't spam it.
#              # The check "if len(self.history) >= 2" in _was_hello_recv handles the end state.
#              # But here we need to trigger the next step.
#              
#              # We need to know if we ALREADY sent the fallback.
#              # If we just received the failure, the queue might be empty.
#              if not self.communicators and not self._write_buf:
#                  self._say_hello(self._user, self._pasw, Identificator._RESP2)
#                  
#              return False
# 
#         if Identificator._ERR_UNKNOWN in output:
#              # Fallback to RESP2 succeeded in the sense that server defaulted to RESP2 (implicit).
#              return True
# 
#         raise ConnectionError(output)
# 
# 
#     def _was_hello_recv(self) -> None | bool:
#         """
#         Returns:
#             bool: True if the HELLO command(s) were received.
#         """
#         # Empty history.
#         if len(self.history) <= 0:
#             return False
# 
#         # Either `HELLO 3 ...` was accepted and received alongside other user command.
#         # Or `HELLO 3 ...` and `HELLO 2 ...` were received.
#         if len(self.history) >= 2:
#             return True
#         
#         # We know the first command is always the `HELLO 3 ...`.
#         assert len(self.history) == 1
#         dialog = self.history[0]
#         assert Identificator._HELLO_CMD in dialog.cmd
#         
#         if isinstance(dialog.output_node, OutputMap):
#             # The server supports RESP3.
#             # No subsequent HELLO command will be sent.
#             return True
#         
#         # The server does NOT support RESP3.
#         # The second command is `HELLO 2 ...` and was not yet sent.
#         return False

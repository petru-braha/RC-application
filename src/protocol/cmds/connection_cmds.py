from frozendict import frozendict
from .types import Args, Opts, CmdDict

CONNECTION_CMDS: CmdDict = frozendict({
    "PING": Opts(None),
    "QUIT": Args()
})
"""
Predefined set storing Connection specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands//#connection-commands
"""

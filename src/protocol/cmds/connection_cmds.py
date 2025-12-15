from frozendict import frozendict

from .patterns import CmdDict, Vitals, Opts, ArgEzz

CONNECTION_CMDS: CmdDict = frozendict({
    "PING": Opts(ArgEzz()),
    "QUIT": Vitals()
})
"""
Predefined set storing Connection specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands//#connection-commands
"""

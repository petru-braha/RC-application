from frozendict import frozendict

from .patterns import CmdDict, Vitals, Opts, ArgEzz, ArgInt, \
                      AUTH_ARG, \
                      SETNAME_ARG

CONNECTION_CMDS: CmdDict = frozendict({
    "HELLO": (Vitals(),
              Opts(ArgInt(),
                   Opts(AUTH_ARG, ArgEzz(), ArgEzz()),
                   Opts(SETNAME_ARG, ArgEzz()))),
    "PING": Opts(ArgEzz()),
    "QUIT": Vitals()
})
"""
Predefined set storing Connection specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands//#connection-commands
"""

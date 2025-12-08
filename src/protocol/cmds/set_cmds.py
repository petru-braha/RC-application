from frozendict import frozendict
from .types import Args, Opts, IntArg, OptKeys, CmdDict
from .list_cmds import COUNT_KEY

LIMIT_KEY: OptKeys = frozenset({"LIMIT"})
MATCH_KEY: OptKeys = frozenset({"MATCH"})

SET_CMDS: CmdDict = frozendict({
    "SADD":  (Args(None, None),
              Opts(None, is_variadic=True)),
    "SCARD":  Args(None),
    "SDIFF": (Args(None),
              Opts(None, is_variadic=True)),
    "SDIFFSTORE": (Args(None, None),
                   Opts(None, is_variadic=True)),
    "SINTER": (Args(None),
               Opts(None, is_variadic=True)),
    "SINTERCARD":  (Args(IntArg(), None),
                    Opts(None, is_variadic=True),
                    Opts(IntArg(), key=LIMIT_KEY)),
    "SINTERSTORE": (Args(None, None),
                    Opts(None, is_variadic=True)),
    "SISMEMBER": Args(None, None),
    "SMEMBERS":  Args(None),
    "SMISMEMBER": (Args(None, None),
                   Opts(None, is_variadic=True)),
    "SMOVE": Args(None, None, None),
    "SPOP": (Args(None),
             Opts(IntArg())),
    "SRANDMEMBER": (Args(None),
                    Opts(IntArg())),
    "SREM": (Args(None, None),
             Opts(None, is_variadic=True)),
    "SSCAN": (Args(None, None),
              Opts(None, key=MATCH_KEY),
              Opts(IntArg(), key=COUNT_KEY)),
    "SUNION": (Args(None),
               Opts(None, is_variadic=True)),
    "SUNIONSTORE": (Args(None, None),
                    Opts(None, is_variadic=True)),
})
"""
Predefined set storing Set specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#set-commands
"""

from frozendict import frozendict
from .types import Args, Opts, IntArg, StrArg, OptKeys, CmdDict

DIRECTION_ARG = StrArg("LEFT", "RIGHT")
POSITION_ARG = StrArg("BEFORE", "AFTER")

COUNT_KEY: OptKeys = frozenset({"COUNT"})
RANK_KEY: OptKeys = frozenset({"RANK"})
MAXLEN_KEY: OptKeys = frozenset({"MAXLEN"})

LIST_CMDS: CmdDict = frozendict({
    "BLMOVE": Args(None, None,
                   DIRECTION_ARG,
                   DIRECTION_ARG,
                   IntArg()),
    "BLMPOP": (Args(IntArg(), IntArg(), None),
               Opts(None, is_variadic=True),
               DIRECTION_ARG,
               Opts(IntArg(), key=COUNT_KEY)),
    "BLPOP":  (Args(None),
               Opts(None, is_variadic=True),
               Args(IntArg())),
    "BRPOP":  (Args(None),
               Opts(None, is_variadic=True),
               Args(IntArg())),
    "BRPOPLPUSH": Args(None, None, IntArg()),
    "LINDEX":  Args(None, IntArg()),
    "LINSERT": Args(None, POSITION_ARG, IntArg(), None),
    "LLEN":    Args(None),
    "LMOVE":   Args(None, None, DIRECTION_ARG, DIRECTION_ARG),
    "LMPOP":  (Args(IntArg(), None),
               Opts(None, is_variadic=True),
               DIRECTION_ARG,
               Opts(IntArg(), key=COUNT_KEY)),
    "LPOP":   (Args(None),
               Opts(IntArg())),
    "LPOS":   (Args(None, None),
               Opts(IntArg(), key=RANK_KEY),
               Opts(IntArg(), key=COUNT_KEY),
               Opts(IntArg(), key=MAXLEN_KEY)),
    "LPUSH":  (Args(None, None),
               Opts(None, is_variadic=True)),
    "LPUSHX": (Args(None, None),
               Opts(None, is_variadic=True)),
    "LRANGE":  Args(None, IntArg(), IntArg()),
    "LREM": Args(None, IntArg(), None),
    "LSET": Args(None, IntArg(), None),
    "LTRIM": Args(None, IntArg(), IntArg()),
    "RPOP": (Args(None),
             Opts(IntArg())),
    "RPOPLPUSH": Args(None, None),
    "RPUSH":  (Args(None, None),
               Opts(None, is_variadic=True)),
    "RPUSHX": (Args(None, None),
               Opts(None, is_variadic=True)),
})
"""
Predefined set storing List specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#list-commands
"""

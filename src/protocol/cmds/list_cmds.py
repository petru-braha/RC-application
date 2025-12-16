from frozendict import frozendict

from .patterns import CmdDict, \
                      Vitals, Opts, Variadic, Opts, \
                      ArgEzz, ArgInt, \
                      DIRECTION_ARGS, \
                      POSITION_ARGS, \
                      COUNT_ARG, \
                      RANK_ARG, \
                      MAXLEN_ARG

LIST_CMDS: CmdDict = frozendict({
    "BLMOVE": Vitals(ArgEzz(), ArgEzz(),
                   DIRECTION_ARGS,
                   DIRECTION_ARGS,
                   ArgInt()),
    "BLMPOP": (Vitals(ArgInt(), ArgInt(), ArgEzz()),
               Variadic(ArgEzz()),
               DIRECTION_ARGS,
               Opts(COUNT_ARG, ArgInt())),
    "BLPOP":  (Vitals(ArgEzz()),
               Variadic(ArgEzz()),
               Vitals(ArgInt())),
    "BRPOP":  (Vitals(ArgEzz()),
               Variadic(ArgEzz()),
               Vitals(ArgInt())),
    "BRPOPLPUSH": Vitals(ArgEzz(), ArgEzz(), ArgInt()),
    "LINDEX":  Vitals(ArgEzz(), ArgInt()),
    "LINSERT": Vitals(ArgEzz(), POSITION_ARGS, ArgInt(), ArgEzz()),
    "LLEN":    Vitals(ArgEzz()),
    "LMOVE":   Vitals(ArgEzz(), ArgEzz(), DIRECTION_ARGS, DIRECTION_ARGS),
    "LMPOP":  (Vitals(ArgInt(), ArgEzz()),
               Variadic(ArgEzz()),
               DIRECTION_ARGS,
               Opts(COUNT_ARG, ArgInt())),
    "LPOP":   (Vitals(ArgEzz()),
               Opts(ArgInt())),
    "LPOS":   (Vitals(ArgEzz(), ArgEzz()),
               Opts(RANK_ARG, ArgInt()),
               Opts(COUNT_ARG, ArgInt()),
               Opts(MAXLEN_ARG, ArgInt())),
    "LPUSH":  (Vitals(ArgEzz(), ArgEzz()),
               Variadic(ArgEzz())),
    "LPUSHX": (Vitals(ArgEzz(), ArgEzz()),
               Variadic(ArgEzz())),
    "LRANGE":  Vitals(ArgEzz(), ArgInt(), ArgInt()),
    "LREM": Vitals(ArgEzz(), ArgInt(), ArgEzz()),
    "LSET": Vitals(ArgEzz(), ArgInt(), ArgEzz()),
    "LTRIM": Vitals(ArgEzz(), ArgInt(), ArgInt()),
    "RPOP": (Vitals(ArgEzz()),
             Opts(ArgInt())),
    "RPOPLPUSH": Vitals(ArgEzz(), ArgEzz()),
    "RPUSH":  (Vitals(ArgEzz(), ArgEzz()),
               Variadic(ArgEzz())),
    "RPUSHX": (Vitals(ArgEzz(), ArgEzz()),
               Variadic(ArgEzz())),
})
"""
Predefined set storing List specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#list-commands
"""

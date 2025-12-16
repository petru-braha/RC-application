from frozendict import frozendict

from .patterns import CmdDict, \
                      Vitals, Variadic, Opts, OptSet, \
                      ArgEzz, ArgInt, ArgFlt, \
                      COMPARISON_ARGS, \
                      PERSISTENCE_ARGS, \
                      PRESENCE_ARGS, \
                      PERSIST_ARG, \
                      LEN_ARG, \
                      IDX_ARG, \
                      MINMATCHLEN_ARG, \
                      WITHMATCHLEN_ARG, \
                      KEEPTTL_ARG, \
                      GET_ARG

STRING_CMDS: CmdDict = frozendict({
    "APPEND": Vitals(ArgEzz(), ArgEzz()),
    "DECR":   Vitals(ArgEzz()),
    "DECRBY": Vitals(ArgEzz(), ArgEzz()),
    "DELEX": (Vitals(ArgEzz()),
              Opts(COMPARISON_ARGS, ArgInt())),
    "DIGEST": Vitals(ArgEzz()),
    "GET":    Vitals(ArgEzz()),
    "GETDEL": Vitals(ArgEzz()),
    "GETEX": (Vitals(ArgEzz()),
              OptSet(Opts(COMPARISON_ARGS, ArgInt()),
                     Opts(PERSIST_ARG))),
    "GETRANGE": Vitals(ArgEzz(), ArgInt(), ArgInt()),
    "GETSET": Vitals(ArgEzz(), ArgEzz()),
    "INCR":   Vitals(ArgEzz()),
    "INCRBY": Vitals(ArgEzz(), ArgInt()),
    "INCRBYFLOAT": Vitals(ArgEzz(), ArgFlt()),
    "LCS":  (Vitals(ArgEzz(), ArgEzz()),
             Opts(LEN_ARG),
             Opts(IDX_ARG),
             Opts(MINMATCHLEN_ARG, ArgInt()),
             Opts(WITHMATCHLEN_ARG)),
    "MGET": (Vitals(ArgEzz()),
             Variadic(ArgEzz())),
    "MSET": (Vitals(ArgEzz(), ArgEzz()),
             Variadic(ArgEzz(), ArgEzz())),
    "MSETEX": (Vitals(ArgInt(), ArgEzz(), ArgEzz()),
               Variadic(ArgEzz(), ArgEzz()),
               Opts(PRESENCE_ARGS),
               OptSet(Opts(PERSISTENCE_ARGS, ArgInt()),
                      Opts(KEEPTTL_ARG))),
    "MSETNX": (Vitals(ArgEzz(), ArgEzz()),
               Variadic(ArgEzz(), ArgEzz())),
    "PSETEX":  Vitals(ArgEzz(), ArgInt(), ArgEzz()),
    "SET":    (Vitals(ArgEzz(), ArgEzz()),
               OptSet(Opts(PRESENCE_ARGS),
                      Opts(COMPARISON_ARGS, ArgInt())),
               Opts(GET_ARG),
               OptSet(Opts(PERSISTENCE_ARGS, ArgInt()),
                      Opts(KEEPTTL_ARG))),
    "SETEX": Vitals(ArgEzz(), ArgInt(), ArgEzz()),
    "SETNX": Vitals(ArgEzz(), ArgEzz()),
    "SETRANGE": Vitals(ArgEzz(), ArgInt(), ArgEzz()),
    "STRLEN": Vitals(ArgEzz()),
    "SUBSTR": Vitals(ArgEzz(), ArgInt(), ArgInt())
})
"""
Predefined set storing String specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#string-commands
"""

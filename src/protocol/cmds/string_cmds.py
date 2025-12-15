from frozendict import frozendict

from .patterns import CmdDict, \
                      Vitals, Variadic, KdOpts, OptSet, \
                      ArgEzz, ArgInt, ArgFlt, OptKey, \
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
              KdOpts(OptKey(COMPARISON_ARGS), ArgInt())),
    "DIGEST": Vitals(ArgEzz()),
    "GET":    Vitals(ArgEzz()),
    "GETDEL": Vitals(ArgEzz()),
    "GETEX": (Vitals(ArgEzz()),
              OptSet(KdOpts(OptKey(COMPARISON_ARGS), ArgInt()),
                     KdOpts(OptKey(PERSIST_ARG)))),
    "GETRANGE": Vitals(ArgEzz(), ArgInt(), ArgInt()),
    "GETSET": Vitals(ArgEzz(), ArgEzz()),
    "INCR":   Vitals(ArgEzz()),
    "INCRBY": Vitals(ArgEzz(), ArgInt()),
    "INCRBYFLOAT": Vitals(ArgEzz(), ArgFlt()),
    "LCS":  (Vitals(ArgEzz(), ArgEzz()),
             KdOpts(OptKey(LEN_ARG)),
             KdOpts(OptKey(IDX_ARG)),
             KdOpts(OptKey(MINMATCHLEN_ARG), ArgInt()),
             KdOpts(OptKey(WITHMATCHLEN_ARG))),
    "MGET": (Vitals(ArgEzz()),
             Variadic(ArgEzz())),
    "MSET": (Vitals(ArgEzz(), ArgEzz()),
             Variadic(ArgEzz(), ArgEzz())),
    "MSETEX": (Vitals(ArgInt(), ArgEzz(), ArgEzz()),
               Variadic(ArgEzz(), ArgEzz()),
               KdOpts(OptKey(PRESENCE_ARGS)),
               OptSet(KdOpts(OptKey(PERSISTENCE_ARGS), ArgInt()),
                      KdOpts(OptKey(KEEPTTL_ARG)))),
    "MSETNX": (Vitals(ArgEzz(), ArgEzz()),
               Variadic(ArgEzz(), ArgEzz())),
    "PSETEX":  Vitals(ArgEzz(), ArgInt(), ArgEzz()),
    "SET":    (Vitals(ArgEzz(), ArgEzz()),
               OptSet(KdOpts(OptKey(PRESENCE_ARGS)),
                      KdOpts(OptKey(COMPARISON_ARGS), ArgInt())),
               KdOpts(OptKey(GET_ARG)),
               OptSet(KdOpts(OptKey(PERSISTENCE_ARGS), ArgInt()),
                      KdOpts(OptKey(KEEPTTL_ARG)))),
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

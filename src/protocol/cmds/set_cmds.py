from frozendict import frozendict

from .patterns import CmdDict, \
                      Vitals, Opts, Variadic, KdOpts, \
                      ArgEzz, ArgInt, OptKey, \
                      COUNT_ARG, \
                      LIMIT_ARG, \
                      MATCH_ARG

SET_CMDS: CmdDict = frozendict({
    "SADD":  (Vitals(ArgEzz(), ArgEzz()),
              Variadic(ArgEzz())),
    "SCARD":  Vitals(ArgEzz()),
    "SDIFF": (Vitals(ArgEzz()),
              Variadic(ArgEzz())),
    "SDIFFSTORE": (Vitals(ArgEzz(), ArgEzz()),
                   Variadic(ArgEzz())),
    "SINTER": (Vitals(ArgEzz()),
               Variadic(ArgEzz())),
    "SINTERCARD":  (Vitals(ArgInt(), ArgEzz()),
                    Variadic(ArgEzz()),
                    KdOpts(OptKey(LIMIT_ARG), ArgInt())),
    "SINTERSTORE": (Vitals(ArgEzz(), ArgEzz()),
                    Variadic(ArgEzz())),
    "SISMEMBER": Vitals(ArgEzz(), ArgEzz()),
    "SMEMBERS":  Vitals(ArgEzz()),
    "SMISMEMBER": (Vitals(ArgEzz(), ArgEzz()),
                   Variadic(ArgEzz())),
    "SMOVE": Vitals(ArgEzz(), ArgEzz(), ArgEzz()),
    "SPOP": (Vitals(ArgEzz()),
             Opts(ArgInt())),
    "SRANDMEMBER": (Vitals(ArgEzz()),
                    Opts(ArgInt())),
    "SREM": (Vitals(ArgEzz(), ArgEzz()),
             Variadic(ArgEzz())),
    "SSCAN": (Vitals(ArgEzz(), ArgEzz()),
              KdOpts(OptKey(MATCH_ARG), ArgEzz()),
              KdOpts(OptKey(COUNT_ARG), ArgInt())),
    "SUNION": (Vitals(ArgEzz()),
               Variadic(ArgEzz())),
    "SUNIONSTORE": (Vitals(ArgEzz(), ArgEzz()),
                    Variadic(ArgEzz())),
})
"""
Predefined set storing Set specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#set-commands
"""

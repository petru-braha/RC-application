from frozendict import frozendict

from .patterns import CmdDict, \
                      Vitals, Opts, Variadic, KdOpts, \
                      ArgEzz, ArgInt, ArgFlt, OptKey, \
                      PRESENCE_ARGS, \
                      COUNT_ARG, \
                      MATCH_ARG, \
                      LIMIT_ARG, \
                      COMP_ARGS, \
                      BY_ARGS, \
                      EXTREMITY_ARGS, \
                      AGGREGATE_ARGS, \
                      CH_ARG, \
                      INCR_ARG, \
                      REV_ARG, \
                      WITHSCORES_ARG, \
                      AGGREGATE_ARG, \
                      WEIGHTS_ARG

SORTED_SET_CMDS: CmdDict = frozendict({
    "BZMPOP": (Vitals(ArgInt(), ArgInt(), ArgEzz()),
               Variadic(ArgEzz()),
               Vitals(EXTREMITY_ARGS)),
    "BZPOPMAX": (Vitals(ArgEzz()),
                 Variadic(ArgEzz()),
                 Vitals(ArgInt())),
    "BZPOPMIN": (Vitals(ArgEzz()),
                 Variadic(ArgEzz()),
                 Vitals(ArgInt())),
    "ZADD":  (Vitals(ArgEzz()),
              KdOpts(OptKey(PRESENCE_ARGS)),
              KdOpts(OptKey(COMP_ARGS)),
              KdOpts(OptKey(CH_ARG)),
              KdOpts(OptKey(INCR_ARG)),
              Vitals(ArgFlt(), ArgEzz()),
              Variadic(ArgFlt(), ArgEzz())),
    "ZCARD":  Vitals(ArgEzz()),
    "ZCOUNT": Vitals(ArgEzz(), ArgFlt(), ArgFlt()),
    "ZDIFF": (Vitals(ArgInt(), ArgEzz()),
              Variadic(ArgEzz()),
              KdOpts(OptKey(WITHSCORES_ARG))),
    "ZDIFFSTORE": (Vitals(ArgEzz(), ArgInt(), ArgEzz()),
                   Variadic(ArgEzz())),
    "ZINCRBY": Vitals(ArgEzz(), ArgFlt(), ArgEzz()),
    "ZINTER": (Vitals(ArgInt(), ArgEzz()),
               Variadic(ArgEzz()),
               KdOpts(OptKey(WEIGHTS_ARG), ArgFlt(),
                    Variadic(ArgFlt())),
                KdOpts(OptKey(AGGREGATE_ARG), AGGREGATE_ARGS),
                KdOpts(OptKey(WITHSCORES_ARG))),
    "ZINTERCARD":  (Vitals(ArgInt(), ArgEzz()),
                    Variadic(ArgEzz()),
                    KdOpts(OptKey(LIMIT_ARG), ArgInt())),
    "ZINTERSTORE": (Vitals(ArgEzz(), ArgInt(), ArgEzz()),
                    Variadic(ArgEzz()),
                    Opts(WEIGHTS_ARG, ArgFlt(),
                         Variadic(ArgFlt())),
                    KdOpts(OptKey(AGGREGATE_ARG), AGGREGATE_ARGS)),
    "ZLEXCOUNT": Vitals(ArgEzz(), ArgEzz(), ArgEzz()),
    "ZMPOP": (Vitals(ArgInt(), ArgEzz()),
              Variadic(ArgEzz()),
              Vitals(EXTREMITY_ARGS),
              KdOpts(OptKey(COUNT_ARG), ArgInt())),
    "ZMSCORE": (Vitals(ArgEzz(), ArgEzz()),
                Variadic(ArgEzz())),
    "ZPOPMAX": (Vitals(ArgEzz()),
                Opts(ArgInt())),
    "ZPOPMIN": (Vitals(ArgEzz()),
                Opts(ArgInt())),
    "ZRANDMEMBER": (Vitals(ArgEzz()),
                    Opts(ArgInt(),
                         KdOpts(OptKey(WITHSCORES_ARG)))),
    "ZRANGE": (Vitals(ArgEzz(), ArgInt(), ArgInt()),
               KdOpts(OptKey(BY_ARGS)),
               KdOpts(OptKey(REV_ARG)),
               KdOpts(OptKey(LIMIT_ARG), ArgInt(), ArgInt()),
               KdOpts(OptKey(WITHSCORES_ARG))),
    "ZRANGEBYLEX":   (Vitals(ArgEzz(), ArgEzz(), ArgEzz()),
                      KdOpts(OptKey(LIMIT_ARG), ArgInt(), ArgInt())),
    "ZRANGEBYSCORE": (Vitals(ArgEzz(), ArgEzz(), ArgEzz()),
                      KdOpts(OptKey(WITHSCORES_ARG)),
                      KdOpts(OptKey(LIMIT_ARG), ArgInt(), ArgInt())),
    "ZRANGESTORE": (Vitals(ArgEzz(), ArgEzz(), ArgEzz(), ArgEzz()),
                    KdOpts(OptKey(BY_ARGS)),
                    KdOpts(OptKey(REV_ARG)),
                    KdOpts(OptKey(LIMIT_ARG), ArgInt(), ArgInt())),
    "ZRANK": (Vitals(ArgEzz(), ArgEzz()),
              KdOpts(OptKey(WITHSCORES_ARG))),
    "ZREM":  (Vitals(ArgEzz(), ArgEzz()),
              Variadic(ArgEzz())),
    "ZREMRANGEBYLEX":   Vitals(ArgEzz(), ArgEzz(), ArgEzz()),
    "ZREMRANGEBYRANK":  Vitals(ArgEzz(), ArgInt(), ArgInt()),
    "ZREMRANGEBYSCORE": Vitals(ArgEzz(), ArgFlt(), ArgFlt()),
    "ZREVRANGE": (Vitals(ArgEzz(), ArgInt(), ArgInt()),
                  KdOpts(OptKey(WITHSCORES_ARG))),
    "ZREVRANGEBYLEX":   (Vitals(ArgEzz(), ArgEzz(), ArgEzz()),
                         KdOpts(OptKey(LIMIT_ARG), ArgInt(), ArgInt())),
    "ZREVRANGEBYSCORE": (Vitals(ArgEzz(), ArgFlt(), ArgFlt()),
                         KdOpts(OptKey(WITHSCORES_ARG)),
                         KdOpts(OptKey(LIMIT_ARG), ArgInt(), ArgInt())),
    "ZREVRANK": (Vitals(ArgEzz(), ArgEzz()),
                 KdOpts(OptKey(WITHSCORES_ARG))),
    "ZSCAN":  (Vitals(ArgEzz(), ArgEzz()),
               KdOpts(OptKey(MATCH_ARG), ArgEzz()),
               KdOpts(OptKey(COUNT_ARG), ArgInt())),
    "ZSCORE":  Vitals(ArgEzz(), ArgEzz()),
    "ZUNION": (Vitals(ArgInt(), ArgEzz()),
               Variadic(ArgEzz()),
               Opts(WEIGHTS_ARG, ArgFlt(),
                    Variadic(ArgFlt())),
                KdOpts(OptKey(AGGREGATE_ARGS), AGGREGATE_ARG),
                KdOpts(OptKey(WITHSCORES_ARG))),
    "ZUNIONSTORE": (Vitals(ArgEzz(), ArgInt(), ArgEzz()),
                    Variadic(ArgEzz()),
                    Opts(WEIGHTS_ARG, ArgFlt(),
                         Variadic(ArgFlt())),
                    KdOpts(OptKey(AGGREGATE_ARGS), AGGREGATE_ARG))
})
"""
Predefined set storing Sorted sets specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#sorted-set-commands
"""

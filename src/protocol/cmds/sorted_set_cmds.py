from frozendict import frozendict
from .types import Args, Opts, IntArg, FltArg, StrArg, OptKeys, CmdDict
from .string_cmds import PRESENCE_KEYS
from .list_cmds import COUNT_KEY
from .set_cmds import MATCH_KEY, LIMIT_KEY

COMP_KEYS: OptKeys = frozenset({"LT", "GT"})
CH_KEY: OptKeys = frozenset({"CH"})
INCR_KEY: OptKeys = frozenset({"INCR"})
WITHSCORES_KEY: OptKeys = frozenset({"WITHSCORES"})
AGGREGATE_KEY: OptKeys = frozenset({"AGGREGATE"})
BY_KEY: OptKeys = frozenset({"BYSCORE", "BYLEX"})
REV_KEY: OptKeys = frozenset({"REV"})

EXTREMITY_ARG = StrArg("MIN", "MAX")
WEIGHTS_ARG = StrArg("WEIGHTS")
AGGREGATE_ARG = StrArg("SUM", "MIN", "MAX")

SORTED_SET_CMDS: CmdDict = frozendict({
    "BZMPOP": (Args(IntArg(), IntArg(), None),
               Opts(None, is_variadic=True),
               Args(EXTREMITY_ARG)),
    "BZPOPMAX": (Args(None),
                 Opts(None, is_variadic=True),
                 Args(IntArg())),
    "BZPOPMIN": (Args(None),
                 Opts(None, is_variadic=True),
                 Args(IntArg())),
    "ZADD":  (Args(None),
              Opts(key=PRESENCE_KEYS),
              Opts(key=COMP_KEYS),
              Opts(key=CH_KEY),
              Opts(key=INCR_KEY),
              Args(FltArg(), None),
              Opts(FltArg(), None, is_variadic=True)),
    "ZCARD":  Args(None),
    "ZCOUNT": Args(None, FltArg(), FltArg()),
    "ZDIFF": (Args(IntArg(), None),
              Opts(None, is_variadic=True),
              Opts(key=WITHSCORES_KEY)),
    "ZDIFFSTORE": (Args(None, IntArg(), None),
                   Opts(None, is_variadic=True)),
    "ZINCRBY": Args(None, FltArg(), None),
    "ZINTER": (Args(IntArg(), None),
               Opts(None, is_variadic=True),
               Opts(WEIGHTS_ARG, FltArg(),
                    Opts(FltArg(), is_variadic=True)),
                Opts(AGGREGATE_ARG, key=AGGREGATE_KEY),
                Opts(key=WITHSCORES_KEY)),
    "ZINTERCARD":  (Args(IntArg(), None),
                    Opts(None, is_variadic=True),
                    Opts(IntArg(), key=LIMIT_KEY)),
    "ZINTERSTORE": (Args(None, IntArg(), None),
                    Opts(None, is_variadic=True),
                    Opts(WEIGHTS_ARG, FltArg(),
                         Opts(FltArg(), is_variadic=True)),
                    Opts(AGGREGATE_ARG, key=AGGREGATE_KEY)),
    "ZLEXCOUNT": Args(None, None, None),
    "ZMPOP": (Args(IntArg(), None),
              Opts(None, is_variadic=True),
              Args(EXTREMITY_ARG),
              Opts(IntArg(), key=COUNT_KEY)),
    "ZMSCORE": (Args(None, None),
                Opts(None, is_variadic=True)),
    "ZPOPMAX": (Args(None),
                Opts(IntArg())),
    "ZPOPMIN": (Args(None),
                Opts(IntArg())),
    "ZRANDMEMBER": (Args(None),
                    Opts(IntArg(),
                         Opts(key=WITHSCORES_KEY))),
    "ZRANGE": (Args(None, IntArg(), IntArg()),
               Opts(key=BY_KEY),
               Opts(key=REV_KEY),
               Opts(IntArg(), IntArg(), key=LIMIT_KEY),
               Opts(key=WITHSCORES_KEY)),
    "ZRANGEBYLEX":   (Args(None, None, None),
                      Opts(IntArg(), IntArg(), key=LIMIT_KEY)),
    "ZRANGEBYSCORE": (Args(None, None, None),
                      Opts(key=WITHSCORES_KEY),
                      Opts(IntArg(), IntArg(), key=LIMIT_KEY)),
    "ZRANGESTORE": (Args(None, None, None, None),
                    Opts(key=BY_KEY),
                    Opts(key=REV_KEY),
                    Opts(IntArg(), IntArg(), key=LIMIT_KEY)),
    "ZRANK": (Args(None, None),
              Opts(key=WITHSCORES_KEY)),
    "ZREM":  (Args(None, None),
              Opts(None, is_variadic=True)),
    "ZREMRANGEBYLEX":   Args(None, None, None),
    "ZREMRANGEBYRANK":  Args(None, IntArg(), IntArg()),
    "ZREMRANGEBYSCORE": Args(None, FltArg(), FltArg()),
    "ZREVRANGE": (Args(None, IntArg(), IntArg()),
                  Opts(key=WITHSCORES_KEY)),
    "ZREVRANGEBYLEX":   (Args(None, None, None),
                         Opts(IntArg(), IntArg(), key=LIMIT_KEY)),
    "ZREVRANGEBYSCORE": (Args(None, FltArg(), FltArg()),
                         Opts(key=WITHSCORES_KEY),
                         Opts(IntArg(), IntArg(), key=LIMIT_KEY)),
    "ZREVRANK": (Args(None, None),
                 Opts(key=WITHSCORES_KEY)),
    "ZSCAN":  (Args(None, None),
               Opts(None, key=MATCH_KEY),
               Opts(IntArg(), key=COUNT_KEY)),
    "ZSCORE":  Args(None, None),
    "ZUNION": (Args(IntArg(), None),
               Opts(None, is_variadic=True),
               Opts(WEIGHTS_ARG, FltArg(),
                    Opts(FltArg(), is_variadic=True)),
                Opts(AGGREGATE_ARG, key=AGGREGATE_KEY),
                Opts(key=WITHSCORES_KEY)),
    "ZUNIONSTORE": (Args(None, IntArg(), None),
                    Opts(None, is_variadic=True),
                    Opts(WEIGHTS_ARG, FltArg(),
                         Opts(FltArg(), is_variadic=True)),
                    Opts(AGGREGATE_ARG, key=AGGREGATE_KEY))
})
"""
Predefined set storing Sorted sets specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#sorted-set-commands
"""

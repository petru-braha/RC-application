from frozendict import frozendict

from .patterns import CmdDict, \
                      Vitals, Opts, Variadic, KdOpts, OptSet, \
                      ArgEzz, ArgInt, ArgFlt, OptKey, \
                      PERSISTENCE_ARGS, \
                      PERSIST_ARG, \
                      KEEPTTL_ARG, \
                      COUNT_ARG, \
                      MATCH_ARG, \
                      EXPIRE_ARGS, \
                      EXPIRE_FIELD_ARGS, \
                      WITHVALUES_ARG, \
                      NOVALUES_ARG, \
                      FIELDS_ARG

HASH_CMDS: CmdDict = frozendict({
    "HDEL": (Vitals(ArgEzz(), ArgEzz()),
             Variadic(ArgEzz())),
    "HEXISTS":  Vitals(ArgEzz(), ArgEzz()),
    "HEXPIRE": (Vitals(ArgEzz(), ArgInt()),
                KdOpts(OptKey(EXPIRE_ARGS)),
                Vitals(FIELDS_ARG, ArgInt(), ArgEzz()),
                Variadic(ArgEzz())),
    "HEXPIREAT": (Vitals(ArgEzz(), ArgInt()),
                  KdOpts(OptKey(EXPIRE_ARGS)),
                  Vitals(FIELDS_ARG, ArgInt(), ArgEzz()),
                  Variadic(ArgEzz())),
    "HEXPIRETIME": (Vitals(ArgEzz(), FIELDS_ARG, ArgInt(), ArgEzz()),
                    Variadic(ArgEzz())),
    "HGET": Vitals(ArgEzz(), ArgEzz()),
    "HGETALL":  Vitals(ArgEzz()),
    "HGETDEL": (Vitals(ArgEzz(), FIELDS_ARG, ArgInt(), ArgEzz()),
                Variadic(ArgEzz())),
    "HGETEX":  (Vitals(ArgEzz()),
                OptSet(KdOpts(OptKey(PERSISTENCE_ARGS), ArgInt()),
                       KdOpts(OptKey(PERSIST_ARG))),
                Vitals(FIELDS_ARG, ArgInt(), ArgEzz()),
                Variadic(ArgEzz())),
    "HINCRBY":  Vitals(ArgEzz(), ArgEzz(), ArgInt()),
    "HINCRBYFLOAT": Vitals(ArgEzz(), ArgEzz(), ArgFlt()),
    "HKEYS":  Vitals(ArgEzz()),
    "HLEN":   Vitals(ArgEzz()),
    "HMGET": (Vitals(ArgEzz(), ArgEzz()),
              Variadic(ArgEzz())),
    "HMSET": (Vitals(ArgEzz(), ArgEzz(), ArgEzz()),
              Variadic(ArgEzz(), ArgEzz())),
    "HPERSIST": (Vitals(ArgEzz(), FIELDS_ARG, ArgInt(), ArgEzz()),
                 Variadic(ArgEzz())),
    "HPEXPIRE": (Vitals(ArgEzz(), ArgInt()),
                 KdOpts(OptKey(EXPIRE_ARGS)),
                 Vitals(FIELDS_ARG, ArgInt(), ArgEzz()),
                 Variadic(ArgEzz())),
    "HPEXPIREAT": (Vitals(ArgEzz(), ArgInt()),
                   KdOpts(OptKey(EXPIRE_ARGS)),
                   Vitals(FIELDS_ARG, ArgInt(), ArgEzz()),
                   Variadic(ArgEzz())),
    "HPEXPIRETIME": (Vitals(ArgEzz(), FIELDS_ARG, ArgInt(), ArgEzz()),
                     Variadic(ArgEzz())),
    "HPTTL": (Vitals(ArgEzz(), FIELDS_ARG, ArgInt(), ArgEzz()),
              Variadic(ArgEzz())),
    "HRANDFIELD": (Vitals(ArgEzz()),
                   Opts(ArgInt(),
                        KdOpts(OptKey(WITHVALUES_ARG)))),
    "HSCAN": (Vitals(ArgEzz(), ArgEzz()),
              KdOpts(OptKey(MATCH_ARG), ArgEzz()),
              KdOpts(OptKey(COUNT_ARG), ArgInt()),
              KdOpts(OptKey(NOVALUES_ARG))),
    "HSET":  (Vitals(ArgEzz(), ArgEzz(), ArgEzz()),
              Opts(ArgEzz(), ArgEzz())),
    "HSETEX": (Vitals(ArgEzz()),
               KdOpts(OptKey(EXPIRE_FIELD_ARGS)),
               OptSet(KdOpts(OptKey(PERSISTENCE_ARGS), ArgInt()),
                      KdOpts(OptKey(KEEPTTL_ARG))),
                Vitals(FIELDS_ARG, ArgInt(), ArgEzz(), ArgEzz()),
                Variadic(ArgEzz(), ArgEzz())),
    "HSETNX":  Vitals(ArgEzz(), ArgEzz(), ArgEzz()),
    "HSTRLEN": Vitals(ArgEzz(), ArgEzz()),
    "HTTL": (Vitals(ArgEzz(), FIELDS_ARG, ArgInt(), ArgEzz()),
             Variadic(ArgEzz())),
    "HVALS": Vitals(ArgEzz())
})
"""
Predefined set storing Hash specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#hash-commands
"""

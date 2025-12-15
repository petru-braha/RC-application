from frozendict import frozendict

from .patterns import CmdDict, \
                      Vitals, Variadic, KdOpts, OptSet, \
                      ArgEzz, ArgInt, OptKey, \
                      GET_ARG, \
                      COUNT_ARG, \
                      MATCH_ARG, \
                      LIMIT_ARG, \
                      EXPIRE_ARGS, \
                      DB_ARG, \
                      REPLACE_ARG, \
                      COPY_ARG, \
                      KEY_ARGS, \
                      KEYS_ARG, \
                      AUTH_ARG, \
                      AUTH2_ARG, \
                      ABSTTL_ARG, \
                      IDLETIME_ARG, \
                      FREQ_ARG, \
                      TYPE_ARG, \
                      BY_ARG, \
                      ALPHA_ARG, \
                      STORE_ARG, \
                      GET_ARG, \
                      ASC_ARGS

GENERIC_CMDS: CmdDict = frozendict({
    "COPY": (Vitals(ArgEzz(), ArgEzz()),
             KdOpts(OptKey(DB_ARG), ArgEzz()),
             KdOpts(OptKey(REPLACE_ARG))),
    "DEL":  (Vitals(ArgEzz()),
             Variadic(ArgEzz())),
    "DUMP":  Vitals(ArgEzz()),
    "EXISTS": (Vitals(ArgEzz()),
               Variadic(ArgEzz())),
    "EXPIRE": (Vitals(ArgEzz(), ArgInt()),
               KdOpts(OptKey(EXPIRE_ARGS))),
    "EXPIREAT":  (Vitals(ArgEzz(), ArgInt()),
                  KdOpts(OptKey(EXPIRE_ARGS))),
    "EXPIRETIME": Vitals(ArgEzz()),
    "KEYS": Vitals(ArgEzz()),
    "MIGRATE": (Vitals(ArgEzz(), ArgInt(), KEY_ARGS, ArgEzz(), ArgInt()),
                KdOpts(OptKey(COPY_ARG)),
                KdOpts(OptKey(REPLACE_ARG)),
                OptSet(KdOpts(OptKey(AUTH_ARG), ArgEzz()),
                       KdOpts(OptKey(AUTH2_ARG), ArgEzz(), ArgEzz())),
                KdOpts(OptKey(KEYS_ARG), ArgEzz(),
                     Variadic(ArgEzz()))),
    "MOVE": Vitals(ArgEzz(), ArgEzz()),
    "PERSIST":     Vitals(ArgEzz()),
    "PEXPIRE":    (Vitals(ArgEzz(), ArgInt()),
                   KdOpts(OptKey(EXPIRE_ARGS))),
    "PEXPIREAT":  (Vitals(ArgEzz(), ArgInt()),
                   KdOpts(OptKey(EXPIRE_ARGS))),
    "PEXPIRETIME": Vitals(ArgEzz()),
    "PTTL": Vitals(ArgEzz()),
    "RANDOMKEY": Vitals(),
    "RENAME": Vitals(ArgEzz(), ArgEzz()),
    "RENAMENX": Vitals(ArgEzz(), ArgEzz()),
    "RESTORE": (Vitals(ArgEzz(), ArgInt(), ArgEzz()),
                KdOpts(OptKey(REPLACE_ARG)),
                KdOpts(OptKey(ABSTTL_ARG)),
                KdOpts(OptKey(IDLETIME_ARG), ArgInt()),
                KdOpts(OptKey(FREQ_ARG), ArgInt())),
    "SCAN": (Vitals(ArgEzz()),
             KdOpts(OptKey(MATCH_ARG), ArgEzz()),
             KdOpts(OptKey(COUNT_ARG), ArgInt()),
             KdOpts(OptKey(TYPE_ARG), ArgEzz())),
    "SORT": (Vitals(ArgEzz()),
             KdOpts(OptKey(BY_ARG), ArgEzz()),
             KdOpts(OptKey(LIMIT_ARG), ArgInt(), ArgInt()),
             KdOpts(OptKey(GET_ARG),
                    ArgEzz(),
                    Variadic(GET_ARG, ArgEzz())),
              KdOpts(OptKey(ASC_ARGS)),
              KdOpts(OptKey(ALPHA_ARG)),
              KdOpts(OptKey(STORE_ARG), ArgEzz())),
    "SORT_RO": (Vitals(ArgEzz()),
             KdOpts(OptKey(BY_ARG), ArgEzz()),
             KdOpts(OptKey(LIMIT_ARG), ArgInt(), ArgInt()),
             KdOpts(OptKey(GET_ARG),
                    ArgEzz(),
                    Variadic(GET_ARG, ArgEzz())),
              KdOpts(OptKey(ASC_ARGS)),
              KdOpts(OptKey(ALPHA_ARG))),
    "TOUCH": (Vitals(ArgEzz()),
              Variadic(ArgEzz())),
    "TTL":  Vitals(ArgEzz()),
    "TYPE": Vitals(ArgEzz()),
    "UNLINK": (Vitals(ArgEzz()),
               Variadic(ArgEzz())),
    "WAIT": Vitals(ArgInt(), ArgInt()),
    "WAITAOF": Vitals(ArgInt(), ArgInt(), ArgInt()),
})
"""
Predefined set storing Generic commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands//#generic-commands
"""

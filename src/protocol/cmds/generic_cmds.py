from frozendict import frozendict

from .patterns import CmdDict, \
                      Vitals, Variadic, Opts, OptSet, \
                      ArgEzz, ArgInt, \
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
             Opts(DB_ARG, ArgEzz()),
             Opts(REPLACE_ARG)),
    "DEL":  (Vitals(ArgEzz()),
             Variadic(ArgEzz())),
    "DUMP":  Vitals(ArgEzz()),
    "EXISTS": (Vitals(ArgEzz()),
               Variadic(ArgEzz())),
    "EXPIRE": (Vitals(ArgEzz(), ArgInt()),
               Opts(EXPIRE_ARGS)),
    "EXPIREAT":  (Vitals(ArgEzz(), ArgInt()),
                  Opts(EXPIRE_ARGS)),
    "EXPIRETIME": Vitals(ArgEzz()),
    "KEYS": Vitals(ArgEzz()),
    "MIGRATE": (Vitals(ArgEzz(), ArgInt(), KEY_ARGS, ArgEzz(), ArgInt()),
                Opts(COPY_ARG),
                Opts(REPLACE_ARG),
                OptSet(Opts(AUTH_ARG, ArgEzz()),
                       Opts(AUTH2_ARG, ArgEzz(), ArgEzz())),
                Opts(KEYS_ARG, ArgEzz(),
                     Variadic(ArgEzz()))),
    "MOVE": Vitals(ArgEzz(), ArgEzz()),
    "PERSIST":     Vitals(ArgEzz()),
    "PEXPIRE":    (Vitals(ArgEzz(), ArgInt()),
                   Opts(EXPIRE_ARGS)),
    "PEXPIREAT":  (Vitals(ArgEzz(), ArgInt()),
                   Opts(EXPIRE_ARGS)),
    "PEXPIRETIME": Vitals(ArgEzz()),
    "PTTL": Vitals(ArgEzz()),
    "RANDOMKEY": Vitals(),
    "RENAME": Vitals(ArgEzz(), ArgEzz()),
    "RENAMENX": Vitals(ArgEzz(), ArgEzz()),
    "RESTORE": (Vitals(ArgEzz(), ArgInt(), ArgEzz()),
                Opts(REPLACE_ARG),
                Opts(ABSTTL_ARG),
                Opts(IDLETIME_ARG, ArgInt()),
                Opts(FREQ_ARG, ArgInt())),
    "SCAN": (Vitals(ArgEzz()),
             Opts(MATCH_ARG, ArgEzz()),
             Opts(COUNT_ARG, ArgInt()),
             Opts(TYPE_ARG, ArgEzz())),
    "SORT": (Vitals(ArgEzz()),
             Opts(BY_ARG, ArgEzz()),
             Opts(LIMIT_ARG, ArgInt(), ArgInt()),
             Opts(GET_ARG,
                    ArgEzz(),
                    Variadic(GET_ARG, ArgEzz())),
              Opts(ASC_ARGS),
              Opts(ALPHA_ARG),
              Opts(STORE_ARG, ArgEzz())),
    "SORT_RO": (Vitals(ArgEzz()),
             Opts(BY_ARG, ArgEzz()),
             Opts(LIMIT_ARG, ArgInt(), ArgInt()),
             Opts(GET_ARG,
                    ArgEzz(),
                    Variadic(GET_ARG, ArgEzz())),
              Opts(ASC_ARGS),
              Opts(ALPHA_ARG)),
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

from frozendict import frozendict
from .types import Args, Opts, OptSet, IntArg, FltArg, StrArg, OptKeys, CmdDict
from .string_cmds import PERSISTENCE_KEYS, PERSIST_KEY, KEEPTTL_KEY
from .list_cmds import COUNT_KEY
from .set_cmds import MATCH_KEY

EXPIRE_KEYS: OptKeys = frozenset({"NX", "XX", "LT", "GT"})
WITHVALUES_KEY: OptKeys = frozenset({"WITHVALUES"})
NOVALUES_KEY: OptKeys = frozenset({"NOVALUES"})
EXPIRE_FIELD_KEYS: OptKeys = frozenset({"FNX", "FXX"})

FIELDS_ARG = StrArg("FIELDS")

HASH_CMDS: CmdDict = frozendict({
    "HDEL": (Args(None, None),
             Opts(None, is_variadic=True)),
    "HEXISTS":  Args(None, None),
    "HEXPIRE": (Args(None, IntArg()),
                Opts(key=EXPIRE_KEYS),
                Args(FIELDS_ARG, IntArg(), None),
                Opts(None, is_variadic=True)),
    "HEXPIREAT": (Args(None, IntArg()),
                  Opts(key=EXPIRE_KEYS),
                  Args(FIELDS_ARG, IntArg(), None),
                  Opts(None, is_variadic=True)),
    "HEXPIRETIME": (Args(None, FIELDS_ARG, IntArg(), None),
                    Opts(None, is_variadic=True)),
    "HGET": Args(None, None),
    "HGETALL":  Args(None),
    "HGETDEL": (Args(None, FIELDS_ARG, IntArg(), None),
                Opts(None, is_variadic=True)),
    "HGETEX":  (Args(None),
                OptSet(Opts(IntArg(), key=PERSISTENCE_KEYS),
                       Opts(key=PERSIST_KEY)),
                Args(FIELDS_ARG, IntArg(), None),
                Opts(None, is_variadic=True)),
    "HINCRBY":  Args(None, None, IntArg()),
    "HINCRBYFLOAT": Args(None, None, FltArg()),
    "HKEYS":  Args(None),
    "HLEN":   Args(None),
    "HMGET": (Args(None, None),
              Opts(None, is_variadic=True)),
    "HMSET": (Args(None, None, None),
              Opts(None, None, is_variadic=True)),
    "HPERSIST": (Args(None, FIELDS_ARG, IntArg(), None),
                 Opts(None, is_variadic=True)),
    "HPEXPIRE": (Args(None, IntArg()),
                 Opts(key=EXPIRE_KEYS),
                 Args(FIELDS_ARG, IntArg(), None),
                 Opts(None, is_variadic=True)),
    "HPEXPIREAT": (Args(None, IntArg()),
                   Opts(key=EXPIRE_KEYS),
                   Args(FIELDS_ARG, IntArg(), None),
                   Opts(None, is_variadic=True)),
    "HPEXPIRETIME": (Args(None, FIELDS_ARG, IntArg(), None),
                     Opts(None, is_variadic=True)),
    "HPTTL": (Args(None, FIELDS_ARG, IntArg(), None),
              Opts(None, is_variadic=True)),
    "HRANDFIELD": (Args(None),
                   Opts(IntArg(),
                        Opts(key=WITHVALUES_KEY))),
    "HSCAN": (Args(None, None),
              Opts(None, key=MATCH_KEY),
              Opts(IntArg(), key=COUNT_KEY),
              Opts(key=NOVALUES_KEY)),
    "HSET":  (Args(None, None, None),
              Opts(None, None)),
    "HSETEX": (Args(None),
               Opts(key=EXPIRE_FIELD_KEYS),
               OptSet(Opts(IntArg(), key=PERSISTENCE_KEYS),
                      Opts(key=KEEPTTL_KEY)),
                Args(FIELDS_ARG, IntArg(), None, None),
                Opts(None, None, is_variadic=True)),
    "HSETNX":  Args(None, None, None),
    "HSTRLEN": Args(None, None),
    "HTTL": (Args(None, FIELDS_ARG, IntArg(), None),
             Opts(None, is_variadic=True)),
    "HVALS": Args(None)
})
"""
Predefined set storing Hash specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#hash-commands
"""

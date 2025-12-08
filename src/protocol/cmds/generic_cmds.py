from frozendict import frozendict
from .types import Args, Opts, OptSet, IntArg, StrArg, OptKeys, CmdDict
from .string_cmds import GET_KEY
from .list_cmds import COUNT_KEY
from .set_cmds import MATCH_KEY, LIMIT_KEY
from .hash_cmds import EXPIRE_KEYS

DB_KEY: OptKeys = frozenset({"DB"})
REPLACE_KEY: OptKeys = frozenset({"REPLACE"})
COPY_KEY: OptKeys = frozenset({"COPY"})
KEYS_KEY: OptKeys = frozenset({"KEYS"})
AUTH_KEY: OptKeys = frozenset({"AUTH"})
AUTH2_KEY: OptKeys = frozenset({"AUTH2"})
ABSTTL_KEY: OptKeys = frozenset({"ABSTTL"})
IDLETIME_KEY: OptKeys = frozenset({"IDLETIME"})
FREQ_KEY: OptKeys = frozenset({"FREQ"})
TYPE_KEY: OptKeys = frozenset({"TYPE"})
BY_KEY: OptKeys = frozenset({"BY"})
ASC_KEYS: OptKeys = frozenset({"ASC", "DESC"})
ALPHA_KEY: OptKeys = frozenset({"ALPHA"})
STORE_KEY: OptKeys = frozenset({"STORE"})

KEY_ARG = StrArg("key", "")
GET_ARG = StrArg("GET")

GENERIC_CMDS: CmdDict = frozendict({
    "COPY": (Args(None, None),
             Opts(None, key=DB_KEY),
             Opts(key=REPLACE_KEY)),
    "DEL":  (Args(None),
             Opts(None, is_variadic=True)),
    "DUMP":  Args(None),
    "EXISTS": (Args(None),
               Opts(None, is_variadic=True)),
    "EXPIRE": (Args(None, IntArg()),
               Opts(key=EXPIRE_KEYS)),
    "EXPIREAT":  (Args(None, IntArg()),
                  Opts(key=EXPIRE_KEYS)),
    "EXPIRETIME": Args(None),
    "KEYS": Args(None),
    "MIGRATE": (Args(None, IntArg(), KEY_ARG, None, IntArg()),
                Opts(key=COPY_KEY),
                Opts(key=REPLACE_KEY),
                OptSet(Opts(None, key=AUTH_KEY),
                       Opts(None, None, key=AUTH2_KEY)),
                Opts(None,
                     Opts(None, is_variadic=True),
                     key=KEYS_KEY)),
    "MOVE": Args(None, None),
    "PERSIST":     Args(None),
    "PEXPIRE":    (Args(None, IntArg()),
                   Opts(key=EXPIRE_KEYS)),
    "PEXPIREAT":  (Args(None, IntArg()),
                   Opts(key=EXPIRE_KEYS)),
    "PEXPIRETIME": Args(None),
    "PTTL": Args(None),
    "RANDOMKEY": Args(),
    "RENAME": Args(None, None),
    "RENAMENX": Args(None, None),
    "RESTORE": (Args(None, IntArg(), None),
                Opts(key=REPLACE_KEY),
                Opts(key=ABSTTL_KEY),
                Opts(IntArg(), key=IDLETIME_KEY),
                Opts(IntArg(), key=FREQ_KEY)),
    "SCAN": (Args(None),
             Opts(None, key=MATCH_KEY),
             Opts(IntArg(), key=COUNT_KEY),
             Opts(None, key=TYPE_KEY)),
    "SORT": (Args(None),
             Opts(None, key=BY_KEY),
             Opts(IntArg(), IntArg(), key=LIMIT_KEY),
             Opts(None,
                  Opts(GET_ARG, None, is_variadic=True),
                  key=GET_KEY),
              Opts(key=ASC_KEYS),
              Opts(key=ALPHA_KEY),
              Opts(None, key=STORE_KEY)),
    "SORT_RO": (Args(None),
             Opts(None, key=BY_KEY),
             Opts(IntArg(), IntArg(), key=LIMIT_KEY),
             Opts(None,
                  Opts(GET_ARG, None, is_variadic=True),
                  key=GET_KEY),
              Opts(key=ASC_KEYS),
              Opts(key=ALPHA_KEY),
              Opts(None, key=STORE_KEY)),
    "TOUCH": (Args(None),
              Opts(None, is_variadic=True)),
    "TTL":  Args(None),
    "TYPE": Args(None),
    "UNLINK": (Args(None),
               Opts(None, is_variadic=True)),
    "WAIT": Args(IntArg(), IntArg()),
    "WAITAOF": Args(IntArg(), IntArg(), IntArg()),
})
"""
Predefined set storing Generic commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands//#generic-commands
"""

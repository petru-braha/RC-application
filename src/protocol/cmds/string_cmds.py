from frozendict import frozendict
from .types import Args, Opts, OptSet, IntArg, FltArg, OptKeys, CmdDict

COMPARISON_KEYS: OptKeys = frozenset({"IFEQ", "IFNE", "IFDEQ", "IFDNE"})
PERSISTENCE_KEYS: OptKeys = frozenset({"EX", "PX", "EXAT", "PXAT"})
PRESENCE_KEYS: OptKeys = frozenset({"NX", "XX"})

PERSIST_KEY: OptKeys = frozenset({"PERSIST"})
LEN_KEY: OptKeys = frozenset({"LEN"})
IDX_KEY: OptKeys = frozenset({"IDX"})
MINMATCHLEN_KEY: OptKeys = frozenset({"MINMATCHLEN"})
WITHMATCHLEN_KEY: OptKeys = frozenset({"WITHMATCHLEN"})
KEEPTTL_KEY: OptKeys = frozenset({"KEEPTTL"})
GET_KEY: OptKeys = frozenset({"GET"})

STRING_CMDS: CmdDict = frozendict({
    "APPEND": Args(None, None),
    "DECR":   Args(None),
    "DECRBY": Args(None, None),
    "DELEX": (Args(None),
              Opts(IntArg(), key=COMPARISON_KEYS)),
    "DIGEST": Args(None),
    "GET":    Args(None),
    "GETDEL": Args(None),
    "GETEX": (Args(None),
              OptSet(Opts(IntArg(), key=COMPARISON_KEYS),
                     Opts(key=PERSIST_KEY))),
    "GETRANGE": Args(None, IntArg(), IntArg()),
    "GETSET": Args(None, None),
    "INCR":   Args(None),
    "INCRBY": Args(None, IntArg()),
    "INCRBYFLOAT": Args(None, FltArg()),
    "LCS":  (Args(None, None),
             Opts(key=LEN_KEY),
             Opts(key=IDX_KEY),
             Opts(IntArg(), key=MINMATCHLEN_KEY),
             Opts(key=WITHMATCHLEN_KEY)),
    "MGET": (Args(None),
             Opts(None, is_variadic=True)),
    "MSET": (Args(None, None),
             Opts(None, None, is_variadic=True)),
    "MSETEX": (Args(IntArg(), None, None),
               Opts(None, None, is_variadic=True),
               Opts(key=PRESENCE_KEYS),
               OptSet(Opts(IntArg(), key=PERSISTENCE_KEYS),
                      Opts(key=KEEPTTL_KEY))),
    "MSETNX": (Args(None, None),
               Opts(None, None, is_variadic=True)),
    "PSETEX":  Args(None, IntArg(), None),
    "SET":    (Args(None, None),
               OptSet(Opts(key=PRESENCE_KEYS),
                      Opts(IntArg(), key=COMPARISON_KEYS)),
               Opts(key=GET_KEY),
               OptSet(Opts(IntArg(), key=PERSISTENCE_KEYS),
                      Opts(key=KEEPTTL_KEY))),
    "SETEX":   Args(None, IntArg(), None),
    "SETNX":   Args(None, None),
    "SETRANGE": Args(None, IntArg(), None),
    "STRLEN":  Args(None),
    "SUBSTR":  Args(None, IntArg(), IntArg())
})
"""
Predefined set storing String specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#string-commands
"""

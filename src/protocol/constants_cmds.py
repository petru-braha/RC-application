from enum import IntEnum
from frozendict import frozendict

# A convention used in this project:
# Tackled Redis data structures are represented by integers.
# This design can be observed in multiple areas in the source code.
# The primary benefit is efficiency in storage, comparison, and lookup operations, as well as simplified type handling in functions like command validation and encoding.
class RedisDataStructure(IntEnum):
    """
    Redis internal data structures.

    Used for building the `CMD_DS_MAP`.
    
    To not be confused with RESP data types as they serve totally different purpose.
    """
    STRING = 0
    LIST = 1
    SET = 2
    HASH = 3
    SORTED_SET = 4

class ArgType(IntEnum):
    """
    Enumerates the human-typed argument types that can be provided to Redis commands.

    Attributes:
        STRING (int): Represents a string argument.
        INTEGER (int): Represents an integer argument.
        FLOAT (int): Represents a floating-point argument.
    """
    INTEGER = 1
    FLOAT = 2

class CmdDef:
    """
    Represents a Redis command and its argument constraints.

    An object has information about the available options and the arguments structure.

    Used for validation in the sanitizer module.

    Attributes:
        required_args_ds (arr):
            Type constraints for the first non-pair arguments of the command.
            Each element corresponds to an argument; None means no type restriction.
        args_pair_ds (arr):
            Type constraints for arguments taken in pairs (e.g., field/value).
            Each element corresponds to one position in the pair; None means no type restriction.
        opt (arr):
            Array of optional options the command may accept (e.g., "WEIGHTS", "AGGREGATE").
        opt_loc (int):
            Index in the argument list where optional options start.  
            If None, optional options are assumed to appear only at the end of all arguments.
            All options must be consecutive and appear after required argu
    """
    def __init__(self,
                 required_args_ds: list[ArgType | None] | None = None,
                 args_pair_ds: list[ArgType | None] | None = None,
                 opt: list[frozendict[str, int]] | None = None,
                 opt_loc: int | None = None) -> None:
        self.required_args_ds = required_args_ds
        self.required_argc = 0
        if required_args_ds is not None:
            self.required_argc = len(required_args_ds)
        self.args_pair_ds = args_pair_ds
        self.opt = opt
        self.opt_loc = opt_loc

# Functionality specific options.
# Their order of does NOT matter, using a dict is fine.
COMPARISON_OPT = frozendict[str, int]({"IFEQ": 1, "IFNE": 1, "IFDEQ": 1, "IFDNE": 1})
PERSISTENCE_OPT = frozendict({"EX": 1, "PX": 1, "EXAT": 1, "PXAT": 1})
PRESENCE_OPT = frozendict({"NX": 0, "XX": 0})
SUBSTR_OPT = frozendict({"LEN": 0, "IDX": 0, "MINMATCHLEN": 1, "WITHMATCHLEN": 0})

# Command specific options.
# Their order matter so we represent them as arrays.
# Note that frozendict.set() creates a copy of the current dictionary with the new pair.
GETEX_OPT = [PERSISTENCE_OPT.set("PERSIST", 0)]
MSETEX_OPT = [PRESENCE_OPT, PERSISTENCE_OPT.set("KEEPTTL", 0)]
SET_OPT = [COMPARISON_OPT | PRESENCE_OPT, frozendict({"GET": 0}), PERSISTENCE_OPT.set("KEEPTTL", 0)]

STRING_CMDS = frozendict({
    "APPEND": CmdDef([None, None]),
    "DECR": CmdDef([None]),
    "DECRBY": CmdDef([None, ArgType.INTEGER]),
    "DELEX": CmdDef([None], opt=[COMPARISON_OPT]),
    "DIGEST": CmdDef([None]),
    "GET": CmdDef([None]),
    "GETDEL": CmdDef([None]),
    "GETEX": CmdDef([None], opt=GETEX_OPT),
    "GETRANGE": CmdDef([None, ArgType.INTEGER, ArgType.INTEGER]),
    "GETSET": CmdDef([None, None]),
    "INCR": CmdDef([None]),
    "INCRBY": CmdDef([None, ArgType.INTEGER]),
    "INCRBYFLOAT": CmdDef([None, ArgType.FLOAT]),
    "LCS": CmdDef([None, None, None], opt=[SUBSTR_OPT]),
    "MGET": CmdDef([None], [None]),
    "MSET": CmdDef([None, None], [None, None]),
    "MSETEX": CmdDef([ArgType.INTEGER, None, None], [None, None], opt=MSETEX_OPT),
    "MSETNX": CmdDef([None, None], [None, None]),
    "PSETEX": CmdDef([None, ArgType.INTEGER, None]),
    "SET": CmdDef([None, None], opt=SET_OPT),
    "SETEX": CmdDef([None, ArgType.INTEGER, None]),
    "SETNX": CmdDef([None, None]),
    "SETRANGE": CmdDef([None, ArgType.INTEGER, None]),
    "STRLEN": CmdDef([None]),
    "SUBSTR": CmdDef([None, ArgType.INTEGER, ArgType.INTEGER])
})
"""
Predefined set storing String specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#string-commands
"""

LIST_CMDS = frozendict({
    "BLMOVE": CmdDef([None, None, None, None, None]),
    "BLMPOP": CmdDef([ArgType.INTEGER, None], [None, None]),
    "BLPOP": CmdDef([None], [None]),
    "BRPOP": CmdDef([None], [None]),
    "BRPOPLPUSH": CmdDef([None, None, ArgType.INTEGER]),
    "LINDEX": CmdDef([None, ArgType.INTEGER]),
    "LINSERT": CmdDef([None, None, None, None]),
    "LLEN": CmdDef([None]),
    "LMOVE": CmdDef([None, None, None, None, None]),
    "LMPOP": CmdDef([None], [None, None], opt=None),
    "LPOP": CmdDef([None], [ArgType.INTEGER]),
    "LPOS": CmdDef([None, None], [None, None]),
    "LPUSH": CmdDef([None], [None]),
    "LPUSHX": CmdDef([None], [None]),
    "LRANGE": CmdDef([None, ArgType.INTEGER, ArgType.INTEGER]),
    "LREM": CmdDef([None, None, None]),
    "LSET": CmdDef([None, ArgType.INTEGER, None]),
    "LTRIM": CmdDef([None, ArgType.INTEGER, ArgType.INTEGER]),
    "RPOP": CmdDef([None], [ArgType.INTEGER]),
    "RPOPLPUSH": CmdDef([None, None]),
    "RPUSH": CmdDef([None], [None]),
    "RPUSHX": CmdDef([None], [None])
})
"""
Predefined set storing List specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#list-commands
"""

SET_CMDS = frozendict({
    "SADD": CmdDef([None], [None]),
    "SCARD": CmdDef([None]),
    "SDIFF": CmdDef([None], [None]),
    "SDIFFSTORE": CmdDef([None, None], [None]),
    "SINTER": CmdDef([None], [None]),
    "SINTERCARD": CmdDef([None], [None]),
    "SINTERSTORE": CmdDef([None, None], [None]),
    "SISMEMBER": CmdDef([None, None]),
    "SMEMBERS": CmdDef([None]),
    "SMISMEMBER": CmdDef([None], [None]),
    "SMOVE": CmdDef([None, None, None]),
    "SPOP": CmdDef([None], [ArgType.INTEGER]),
    "SRANDMEMBER": CmdDef([None], [ArgType.INTEGER]),
    "SREM": CmdDef([None], [None]),
    "SSCAN": CmdDef([None], [None]),
    "SUNION": CmdDef([None], [None]),
    "SUNIONSTORE": CmdDef([None, None], [None])
})
"""
Predefined set storing Set specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#set-commands
"""

HASH_CMDS = frozendict({
    "HDEL": CmdDef([None], [None]),
    "HEXISTS": CmdDef([None, None]),
    "HEXPIRE": CmdDef([None, ArgType.INTEGER]),
    "HEXPIREAT": CmdDef([None, ArgType.INTEGER]),
    "HEXPIRETIME": CmdDef([None, None]),
    "HGET": CmdDef([None, None]),
    "HGETALL": CmdDef([None]),
    "HGETDEL": CmdDef([None, None]),
    "HGETEX": CmdDef([None, None]),
    "HINCRBY": CmdDef([None, None, ArgType.INTEGER]),
    "HINCRBYFLOAT": CmdDef([None, None, ArgType.FLOAT]),
    "HKEYS": CmdDef([None]),
    "HLEN": CmdDef([None]),
    "HMGET": CmdDef([None], [None]),
    "HMSET": CmdDef([None], [None, None]),
    "HPERSIST": CmdDef([None, None]),
    "HPEXPIRE": CmdDef([None, ArgType.INTEGER]),
    "HPEXPIREAT": CmdDef([None, ArgType.INTEGER]),
    "HPEXPIRETIME": CmdDef([None, None]),
    "HPTTL": CmdDef([None]),
    "HRANDFIELD": CmdDef([None], [None]),
    "HSCAN": CmdDef([None], [None]),
    "HSET": CmdDef([None], [None, None]),
    "HSETEX": CmdDef([None, None, None]),
    "HSETNX": CmdDef([None, None, None]),
    "HSTRLEN": CmdDef([None, None]),
    "HTTL": CmdDef([None]),
    "HVALS": CmdDef([None])
})
"""
Predefined set storing Hash specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#hash-commands
"""

SORTED_SET_CMDS = frozendict({
    "BZMPOP": CmdDef([None], [None, ArgType.INTEGER]),
    "BZPOPMAX": CmdDef([None], [None, ArgType.INTEGER]),
    "BZPOPMIN": CmdDef([None], [None, ArgType.INTEGER]),
    "ZADD": CmdDef([None], [ArgType.FLOAT, None]),
    "ZCARD": CmdDef([None]),
    "ZCOUNT": CmdDef([None, ArgType.FLOAT, ArgType.FLOAT]),
    "ZDIFF": CmdDef([ArgType.INTEGER], [None]),
    "ZDIFFSTORE": CmdDef([None, ArgType.INTEGER], [None]),
    "ZINCRBY": CmdDef([None, ArgType.FLOAT, None]),
    "ZINTER": CmdDef([ArgType.INTEGER], [None]),
    "ZINTERCARD": CmdDef([ArgType.INTEGER, ArgType.INTEGER], [None]),
    "ZINTERSTORE": CmdDef([None, ArgType.INTEGER], [None]),
    "ZLEXCOUNT": CmdDef([None, None, None]),
    "ZMPOP": CmdDef([None], [None, ArgType.INTEGER]),
    "ZMSCORE": CmdDef([None], [None]),
    "ZPOPMAX": CmdDef([None], [ArgType.INTEGER]),
    "ZPOPMIN": CmdDef([None], [ArgType.INTEGER]),
    "ZRANDMEMBER": CmdDef([None], [ArgType.INTEGER]),
    "ZRANGE": CmdDef([None, ArgType.INTEGER, ArgType.INTEGER]),
    "ZRANGEBYLEX": CmdDef([None, None, None]),
    "ZRANGEBYSCORE": CmdDef([None, ArgType.FLOAT, ArgType.FLOAT]),
    "ZRANGESTORE": CmdDef([None, None, ArgType.INTEGER, ArgType.INTEGER], [None, ArgType.FLOAT]),
    "ZRANK": CmdDef([None, None]),
    "ZREM": CmdDef([None], [None]),
    "ZREMRANGEBYLEX": CmdDef([None, None, None]),
    "ZREMRANGEBYRANK": CmdDef([None, ArgType.INTEGER, ArgType.INTEGER]),
    "ZREMRANGEBYSCORE": CmdDef([None, ArgType.FLOAT, ArgType.FLOAT]),
    "ZREVRANGE": CmdDef([None, ArgType.INTEGER, ArgType.INTEGER]),
    "ZREVRANGEBYLEX": CmdDef([None, None, None]),
    "ZREVRANGEBYSCORE": CmdDef([None, ArgType.FLOAT, ArgType.FLOAT]),
    "ZREVRANK": CmdDef([None, None]),
    "ZSCAN": CmdDef([None], [None]),
    "ZSCORE": CmdDef([None, None]),
    "ZUNION": CmdDef([ArgType.INTEGER], [None]),
    "ZUNIONSTORE": CmdDef([None, ArgType.INTEGER], [None])
})
"""
Predefined set storing Sorted sets specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#sorted-set-commands
"""

CONNECTION_CMDS = frozendict({
    "PING": CmdDef(),
    "QUIT": CmdDef()
})
"""
Predefined set storing Connection specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands//#connection-commands
"""

GENERIC_CMDS = frozendict({
    "COPY": CmdDef([None, None]),
    "DEL": CmdDef([None], [None]),
    "DUMP": CmdDef([None]),
    "EXISTS": CmdDef([None], [None]),
    "EXPIRE": CmdDef([None, ArgType.INTEGER]),
    "EXPIREAT": CmdDef([None, ArgType.INTEGER]),
    "EXPIRETIME": CmdDef([None]),
    "KEYS": CmdDef([None]),
    "MIGRATE": CmdDef([None, None, None, None, ArgType.INTEGER]),
    "MOVE": CmdDef([None, ArgType.INTEGER]),
    "PERSIST": CmdDef([None]),
    "PEXPIRE": CmdDef([None, ArgType.INTEGER]),
    "PEXPIREAT": CmdDef([None, ArgType.INTEGER]),
    "PEXPIRETIME": CmdDef([None]),
    "PTTL": CmdDef([None]),
    "RANDOMKEY": CmdDef(),
    "RENAME": CmdDef([None, None]),
    "RENAMENX": CmdDef([None, None]),
    "RESTORE": CmdDef([None, None, None]),
    "SCAN": CmdDef([ArgType.INTEGER], [None]),
    "SORT": CmdDef([None], opt=[frozendict({"BY": 1, "GET": 1, "LIMIT": 2, "ASC": 0, "DESC": 0, "ALPHA": 0})], opt_loc=1),
    "SORT_RO": CmdDef([None], opt=[frozendict({"BY": 1, "GET": 1, "LIMIT": 2, "ASC": 0, "DESC": 0, "ALPHA": 0})], opt_loc=1),
    "TOUCH": CmdDef([None], [None]),
    "TTL": CmdDef([None]),
    "TYPE": CmdDef([None]),
    "UNLINK": CmdDef([None], [None]),
    "WAIT": CmdDef([ArgType.INTEGER, ArgType.INTEGER]),
    "WAITAOF": CmdDef([ArgType.INTEGER, ArgType.INTEGER]),
})
"""
Predefined set storing Generic commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands//#generic-commands
"""

CMDS = (STRING_CMDS, LIST_CMDS, SET_CMDS, HASH_CMDS, SORTED_SET_CMDS, CONNECTION_CMDS, GENERIC_CMDS)
"""
All comands in a single variable.
"""

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

STRING_CMDS = frozenset([
    "APPEND", "DECR", "DECRBY", "DELEX", "DIGEST", "GET", "GETDEL", "GETEX", "GETRANGE",
    "GETSET", "INCR", "INCRBY", "INCRBYFLOAT", "LCS", "MGET", "MSET", "MSETEX",
    "MSETNX", "PSETEX", "SET", "SETEX", "SETNX", "SETRANGE", "STRLEN", "SUBSTR"
])
"""
Predefined set storing String specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#string-commands
"""

LIST_CMDS = frozenset([
    "BLMOVE", "BLMPOP", "BLPOP", "BRPOP", "BRPOPLPUSH", "LINDEX", "LINSERT", "LLEN",
    "LMOVE", "LMPOP", "LPOP", "LPOS", "LPUSH", "LPUSHX", "LRANGE", "LREM", "LSET",
    "LTRIM", "RPOP", "RPOPLPUSH", "RPUSH", "RPUSHX"
])
"""
Predefined set storing List specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#list-commands
"""

SET_CMDS = frozenset([
    "SADD", "SCARD", "SDIFF", "SDIFFSTORE", "SINTER", "SINTERCARD", "SINTERSTORE",
    "SISMEMBER", "SMEMBERS", "SMISMEMBER", "SMOVE", "SPOP", "SRANDMEMBER", "SREM",
    "SSCAN", "SUNION", "SUNIONSTORE"
])
"""
Predefined set storing Set specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#set-commands
"""

HASH_CMDS = frozenset([
    "HDEL", "HEXISTS", "HEXPIRE", "HEXPIREAT", "HEXPIRETIME", "HGET", "HGETALL", "HGETDEL",
    "HGETEX", "HINCRBY", "HINCRBYFLOAT", "HKEYS", "HLEN", "HMGET", "HMSET", "HPERSIST",
    "HPEXPIRE", "HPEXPIREAT", "HPEXPIRETIME", "HPTTL", "HRANDFIELD", "HSCAN", "HSET",
    "HSETEX", "HSETNX", "HSTRLEN", "HTTL", "HVALS"
])
"""
Predefined set storing Hash specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#hash-commands
"""

SORTED_SET_CMDS = frozenset([
    "BZMPOP", "BZPOPMAX", "BZPOPMIN", "ZADD", "ZCARD", "ZCOUNT", "ZDIFF", "ZDIFFSTORE",
    "ZINCRBY", "ZINTER", "ZINTERCARD", "ZINTERSTORE", "ZLEXCOUNT", "ZMPOP", "ZMSCORE",
    "ZPOPMAX", "ZPOPMIN", "ZRANDMEMBER", "ZRANGE", "ZRANGEBYLEX", "ZRANGEBYSCORE",
    "ZRANGESTORE", "ZRANK", "ZREM", "ZREMRANGEBYLEX", "ZREMRANGEBYRANK", "ZREMRANGEBYSCORE",
    "ZREVRANGE", "ZREVRANGEBYLEX", "ZREVRANGEBYSCORE", "ZREVRANK", "ZSCAN", "ZSCORE",
    "ZUNION", "ZUNIONSTORE"
])
"""
Predefined set storing Sorted sets specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands/#sorted-set-commands
"""

CMD_DS_MAP = frozendict({
    cmd: data_type
    for cmd_list, data_type in [
        (STRING_CMDS, RedisDataStructure.STRING),
        (LIST_CMDS, RedisDataStructure.LIST),
        (SET_CMDS, RedisDataStructure.SET),
        (HASH_CMDS, RedisDataStructure.HASH),
        (SORTED_SET_CMDS, RedisDataStructure.SORTED_SET),
    ]
    for cmd in cmd_list
})
"""
Predefined dictionary mapping commands to their specific data-type.

Used for user input parsing to validate the given command and to retrieve its corresponding data type.
"""

CONNECTION_CMDS = frozenset(["PING", "QUIT"])
"""
Predefined set storing Connection specific commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands//#connection-commands
"""

GENERIC_CMDS = frozenset([
    "COPY", "DEL", "DUMP", "EXISTS", "EXPIRE", "EXPIREAT", "EXPIRETIME", "KEYS",
    "MIGRATE", "MOVE", "OBJECT ENCODING", "OBJECT FREQ", "OBJECT IDLETIME",
    "OBJECT REFCOUNT", "PERSIST", "PEXPIRE", "PEXPIREAT", "PEXPIRETIME",
    "PTTL", "RANDOMKEY", "RENAME", "RENAMENX", "RESTORE",
    "SCAN", "SORT", "SORT_RO", "TOUCH", "TTL", "TYPE", "UNLINK", "WAIT", "WAITAOF"
])
"""
Predefined set storing Generic commands.

See more: https://redis.io/docs/latest/commands/redis-8-4-commands//#generic-commands
"""

# todo minimum argument count

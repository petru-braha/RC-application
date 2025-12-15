from .types import ArgStr, ArgSet

"""
Defines argument pattern constants for command options, categorized by data type.

The organization of this module implies a cascading scope of availability.
Constants defined in earlier sections (e.g., String commands)
are available for reuse by subsequent sections (e.g., List, Hash, or Generic commands).
Command types appearing later in the file may leverage shared option keys
established in preceding categories.
"""

#! String commands options' keys.
COMPARISON_ARGS  = ArgSet("IFEQ", "IFNE", "IFDEQ", "IFDNE")
PERSISTENCE_ARGS = ArgSet("EX", "PX", "EXAT", "PXAT")
PRESENCE_ARGS = ArgSet("NX", "XX")

PERSIST_ARG = ArgStr("PERSIST")
LEN_ARG = ArgStr("LEN")
IDX_ARG = ArgStr("IDX")
MINMATCHLEN_ARG  = ArgStr("MINMATCHLEN")
WITHMATCHLEN_ARG = ArgStr("WITHMATCHLEN")
KEEPTTL_ARG = ArgStr("KEEPTTL")
GET_ARG = ArgStr("GET")

#! List commands options' keys.
DIRECTION_ARGS = ArgSet("LEFT", "RIGHT")
POSITION_ARGS  = ArgSet("BEFORE", "AFTER")

COUNT_ARG  = ArgStr("COUNT")
RANK_ARG   = ArgStr("RANK")
MAXLEN_ARG = ArgStr("MAXLEN")

#! Set commands options' keys.
LIMIT_ARG = ArgStr("LIMIT")
MATCH_ARG = ArgStr("MATCH")

#! Hash commands options' keys.
EXPIRE_ARGS = ArgSet("NX", "XX", "LT", "GT")
EXPIRE_FIELD_ARGS = ArgSet("FNX", "FXX")

WITHVALUES_ARG = ArgStr("WITHVALUES")
NOVALUES_ARG = ArgStr("NOVALUES")
FIELDS_ARG = ArgStr("FIELDS")

#! Sorted Set commands options' keys.
COMP_ARGS = ArgSet("LT", "GT")
BY_ARGS = ArgSet("BYSCORE", "BYLEX")
EXTREMITY_ARGS = ArgSet("MIN", "MAX")
AGGREGATE_ARGS = ArgSet("SUM", "MIN", "MAX")

CH_ARG = ArgStr("CH")
INCR_ARG = ArgStr("INCR")
REV_ARG  = ArgStr("REV")
WITHSCORES_ARG = ArgStr("WITHSCORES")
AGGREGATE_ARG  = ArgStr("AGGREGATE")
WEIGHTS_ARG = ArgStr("WEIGHTS")

#! Generic commands options' keys.
ASC_ARGS = ArgSet("ASC", "DESC")
KEY_ARGS = ArgSet("key", "")

DB_ARG = ArgStr("DB")
REPLACE_ARG = ArgStr("REPLACE")
COPY_ARG = ArgStr("COPY")
KEYS_ARG = ArgStr("KEYS")
AUTH_ARG = ArgStr("AUTH")
AUTH2_ARG = ArgStr("AUTH2")
ABSTTL_ARG = ArgStr("ABSTTL")
IDLETIME_ARG = ArgStr("IDLETIME")
FREQ_ARG = ArgStr("FREQ")
TYPE_ARG = ArgStr("TYPE")
BY_ARG   = ArgStr("BY")
ALPHA_ARG = ArgStr("ALPHA")
STORE_ARG = ArgStr("STORE")
GET_ARG = ArgStr("GET")

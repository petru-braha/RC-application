from frozendict import frozendict

class Arg:
    pass

class IntArg(Arg):
    pass

class FltArg(Arg):
    pass

class StrArg(Arg):
    def __init__(self, *value: str) -> None:
        super().__init__()
        self.values = frozenset({value})

class ArgSection(Arg):
    def __init__(self, argv: list[Arg | None]) -> None:
        self.argv = argv
        self.is_optional = False
        self.is_variadic = False

class Args(ArgSection):
    def __init__(self, *arg: Arg | None) -> None:
        c_list = [c for _, c in enumerate(arg)]
        ArgSection.__init__(self, c_list)

class Opts(ArgSection):
    def __init__(self, *arg: Arg | None,
                 is_variadic: bool = False,
                 key: frozenset[str] | None = None) -> None:
        c_list = [c for _, c in enumerate(arg)]
        ArgSection.__init__(self, c_list)
        self.is_optional = True
        self.is_variadic = is_variadic
        self.key = key

class OptSet(ArgSection):
    def __init__(self, *opts: Opts) -> None:
        Arg.__init__(self)
        self.is_optional = True
        self.is_variadic = False
        self.opt_set = frozenset({opts})

# Mapping from option keyword to needed value count.
OptKeys = frozenset[str]

# Mapping from command name to its definition/constraints.
CmdDict = frozendict[str, tuple[ArgSection]]

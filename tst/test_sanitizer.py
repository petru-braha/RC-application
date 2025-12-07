from unittest import TestCase
from frozendict import frozendict
from src.protocol.sanitizer import _count_opt, _validate_argc, sanitizer
from src.protocol.exceptions import ArgumentCountError
from src.protocol.constants_cmds import CmdDef

class TestSanitizer(TestCase):
    """
    Tests the argument-counting and validation utilities used by the sanitizer.
    """

    def setUp(self):
        # Minimal fake commands for isolated testing.
        # required_argc = n, opt = list[frozendict]
        self.CMD_NO_OPT = CmdDef(
            name="NOOPT",
            required_argc=2,
            opt=None
        )

        # Options: PX needs 1 argument, NX needs 0 arguments
        self.OPT_SET = [
            frozendict({"PX": 1, "NX": 0})
        ]

        self.CMD_WITH_OPT = CmdDef(
            name="OPTSET",
            required_argc=1,
            opt=self.OPT_SET,
        )

        # Fake command dictionary
        self.cmd_dict = frozendict({
            "NOOPT": self.CMD_NO_OPT,
            "OPTSET": self.CMD_WITH_OPT
        })

    # --------------------------------------------------
    # _count_opt
    # --------------------------------------------------

    def test_count_opt_no_opt(self):
        argv = ["key", "value"]
        self.assertEqual(_count_opt(argv, self.CMD_NO_OPT), 0)

    def test_count_opt_single_option(self):
        argv = ["key", "PX", "100"]
        # PX contributes (1 value + option itself) = 2
        self.assertEqual(_count_opt(argv, self.CMD_WITH_OPT), 2)

    def test_count_opt_option_with_zero_values(self):
        argv = ["key", "NX"]
        # NX contributes (0 values + option itself) = 1
        self.assertEqual(_count_opt(argv, self.CMD_WITH_OPT), 1)

    def test_count_opt_multiple_options(self):
        argv = ["key", "PX", "100", "NX"]
        # PX → 2, NX → 1 → total = 3
        self.assertEqual(_count_opt(argv, self.CMD_WITH_OPT), 3)

    # --------------------------------------------------
    # _validate_argc
    # --------------------------------------------------

    def test_validate_argc_valid(self):
        argv = ["a", "b"]
        # NOOPT requires 2 args, no opts used
        _validate_argc("NOOPT", argv, self.cmd_dict)

    def test_validate_argc_missing_required(self):
        argv = ["onlyone"]
        with self.assertRaises(ArgumentCountError):
            _validate_argc("NOOPT", argv, self.cmd_dict)

    def test_validate_argc_optional_must_not_reduce_required(self):
        # required = 2
        # PX consumes itself + 1 value = 2 (ignored), but required args are still missing
        argv = ["PX", "100"]
        with self.assertRaises(ArgumentCountError):
            _validate_argc("NOOPT", argv, self.cmd_dict)

    def test_validate_argc_optional_counting(self):
        # OPTSET requires 1 argument
        # Providing: ["real_arg", "NX"] → NX contributes 1 opt count
        argv = ["real_arg", "NX"]
        _validate_argc("OPTSET", argv, self.cmd_dict)

    # --------------------------------------------------
    # sanitizer (requires mocking CMDS structure)
    # --------------------------------------------------

    def test_sanitizer_invalid_command(self):
        with self.assertRaises(KeyError):
            sanitizer("NONEXISTENT", [])

    def test_sanitizer_connection_cmd_rejects_args(self):
        # This test assumes CONNECTION_CMDS contains at least one command, e.g., "PING".
        # We simulate it here by calling a connection command with args.
        with self.assertRaises(ArgumentCountError):
            sanitizer("PING", ["arg"])

    def test_sanitizer_valid_command(self):
        # Must exist in CMDS in actual code — here we assume it does.
        try:
            sanitizer("SET", ["x", "1"])
        except Exception:
            self.fail("sanitizer() raised unexpectedly for a valid SET command")

    def test_sanitizer_missing_required_arguments(self):
        with self.assertRaises(ArgumentCountError):
            sanitizer("SET", ["only_one_arg"])

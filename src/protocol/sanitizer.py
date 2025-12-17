from src.protocol.cmds import *
from src.protocol.exceptions import ArgumentCountError

from .exceptions import SanitizerError

"""
Terminology:

- section = array of patterns that must be validated.
- interval = argument (sub)list (potentially cut from the original array)

In this module, we search for matching sections in intervals.

One could visualize the initial interval as a big string,
in which we perform substring searches of the sections.
"""

def sanitizer(cmd: str, argv: list[str]) -> None:
    """
    Performs these **input** validations:

    0. tests if the command is valid
    1. verifies that the number of arguments falls within the allowed range for the command
    2. if the command targets a specific Redis data structure, checks that the argument(s) match the expected type(s)

    The actual argument sanitization is performed in `arg_sanitizer()`.

    Raises:
        KeyError: If the command is invalid.
        ArgumentCountError: If the input arguments for an command are either missing or too many.
    """
    cmd_dict_match = None
    for cmd_dict in CMDS:
        if cmd not in cmd_dict:
            continue
        cmd_dict_match = cmd_dict
        break
        
    if cmd_dict_match == None:
        raise KeyError("Command is either not supported or not existent.")
    
    pattern_sections = cmd_dict_match[cmd]
    _RequiredSanitizer(pattern_sections, argv)

# The argument traversal should be incremented only in here.
# Classes inheriting `_ArgumentSanitizer` are responsible for roolback logic.
class _ArgumentSanitizer:
    """
    Base helper class.

    Defines validation logic for a single argument.

    Attributes:
        _arg_idx (int): The argument traversal index.
                        Initialized with 0.
        _argv (arr): The (sub)list of arguments provided.
        _argc (int): The count of the argument list.
    """

    _FOREVER = True

    def __init__(self, argv: list[str]) -> None:
        self._arg_idx = 0
        self._argv = argv
        self._argc = len(argv)
    
    def _process_leaf(self, node: Argument | VariadicKey) -> bool:
        """
        Validates basic argument types (Int, Float, String, ArgSet).

        Returns:
            bool: If the the argument value and type could be matched.
        """
        arg = self._argv[self._arg_idx]
        try:
            if isinstance(node, VariadicKey):
                self._process_arg(node.pattern, arg)
            else:
                self._process_arg(node, arg)
        except TypeError:
            return False
        
        # If validation passed, consume the argument.
        self._arg_idx += 1
        return True

    def _process_arg(self, node: Argument, arg: str) -> None:
        """
        Internal method.

        Makes assertions and runs validation logic of all argument types.
        
        This method should not be used manually.
        See `_process_leaf()`.

        Raises:
            ValueError: if the argument does not its expected type.
        """
        if isinstance(node, ArgEzz):
            pass
        
        elif isinstance(node, ArgInt):
            # Throws ValueError if the string can not be parsed into an int.
            int(arg)
        
        elif isinstance(node, ArgFlt):
            # Throws ValueError if the string can not be parsed into a float.
            float(arg)
        
        if isinstance(node, ArgStr):
            if arg.upper() != node.pattern.upper():
                raise ValueError(f"{arg} must be {node.pattern}.")

        assert isinstance(node, ArgSet)
        for pattern in node.patterns:
            if self._process_leaf(pattern) == True:
                return
        
        # Raised if no match was found between the argument and the pattern set.
        raise ValueError(f"{arg} must be {node.pattern}.")

_OptionAssignmentResult = None | bool
"""
"""
_IS_COMPLETE_VALUE = True
"""
"""
_IS_SKIPPABLE_VALUE = False
"""
"""
_IS_INVALID_VALUE = None
"""
"""

# This class resembles the substring searching problem.
# Given multiple substrings (argument type sections),
# Return if those can form the input **"haystack"**.
class _RequiredSanitizer(_ArgumentSanitizer):
    """
    Tries to match all required sections first.
    If succeeds, it pairs non-matching arguments with potential options.
    
    If both operations fail, the client input is invalid.

    Attributes:
        _all_vitals (arr): The list of all the required matching sections.
        _all_vitals_len (int): The count of the required sections.
        _all_vitals_skips (dict): The dictionary having as key a vital section,
                                 and as value: how many arguments were skipped,
                                 and assigned to prior optional sections.
        _prev_opt_sanitizers (dict): The dictionary having as key a vital section,
                                    and as value an array of optional sections found
                                    before the current one and,
                                    after the previous vital section.
    """
    _FIRST_SECTION_IDX: int = 0
    _NO_SKIPS: int = 0
    
    def __init__(self, pattern_sections: tuple[Section, ...], argv: list[str]) -> None:
        """
        Preprocesses the client input.

        Check if all vital sections can be matched using backtracking.

        Raises:
            SanitizerError: if at least one vital section was not matched.
        """
        all_vitals: list[Vitals] = []
        all_vitals_skips: dict[Vitals, int] = {}
        prev_opt_sanitizers: dict[Vitals, _OptionSanitizer] = {}
        prev_sect: list[OptionalSect] = []
        
        for section in pattern_sections:
            if isinstance(section, OptionalSect):
                prev_sect.append(section)
                continue

            assert isinstance(section, Vitals)
            all_vitals.append(section)
            all_vitals_skips[section] = _RequiredSanitizer._NO_SKIPS
            opt_sanitizer = _OptionSanitizer(prev_sect, argv)
            prev_opt_sanitizers[section] = opt_sanitizer
            prev_sect = []

        super().__init__(argv)
        self._all_vitals = all_vitals
        self._all_vitals_len = len(all_vitals)
        self._all_vitals_skips = all_vitals_skips
        self._prev_opt_sanitizers = prev_opt_sanitizers

        if not self._is_matching(_RequiredSanitizer._FIRST_SECTION_IDX):
            raise
    
    def _is_matching(self, vitals_idx: int) -> bool:
        """
        Goes through each vital and optional sections and tries to validate it.

        Parameters:
            vitals_idx (int): Vital section index.

        Returns:
            bool: if all sections were correctly matched,
                  and no argument was left unpaired.
        """
        # Check if all validation sections were consumed.
        if vitals_idx >= self._all_vitals_len:
            return True
        
        while _RequiredSanitizer._FOREVER:
            if not self._traverse_vitals(self._all_vitals[vitals_idx]):
                self.assign_option(vitals_idx)
                if self._last_status == _IS_INVALID_VALUE:
                    return False
                continue

            start_idx = self._arg_idx
            if self._last_status == _IS_COMPLETE_VALUE:
                if self._is_matching(vitals_idx + 1):
                    return True
            
            # The backtrack step.
            # The upcoming vitals were not validated.
            self._arg_idx = start_idx
            # While the current vitals were validated,
            # It does not represent a full solution,
            # So it is being dropped.
            self.assign_option(vitals_idx)
            if self._last_status == _IS_INVALID_VALUE:
                return False
    
    def _traverse_vitals(self, node: Vitals) -> bool:
        """
        Strictly validates a sequence of required patterns.

        Returns:
            bool: If the constraint sequence was matched.
        """
        if self._arg_idx + len(node.patterns) >= self._argc:
            return False
        
        start_idx = self._arg_idx
        for pattern in node.patterns:
            if self._process_leaf(pattern) == False:
                self._arg_idx = start_idx
                return False
        
        return True
    
    # assign it to current sections prior optionals
    def assign_option(self, vitals_idx) -> None:
        """
        Check if the current argument can be skipped,
        from being matched to a vital section.
        Assign it to a prior optional section instead, if possible.

        Returns:
            bool: If the current argument can be skipped.
        """
        vitals = self._all_vitals[vitals_idx]

        self._all_vitals_skips[vitals] += 1
        skips = self._all_vitals_skips[vitals]
        end_idx = self._arg_idx + skips
        subinternal = self._argv[self._arg_idx:end_idx]
        
        option_sanitizer = self._prev_opt_sanitizers[vitals_idx]
        self._last_status = option_sanitizer._set_argv(subinternal)

# The goal of this class is to find the subarray of arguments in the optional lists.
class _OptionSanitizer(_ArgumentSanitizer):
    """
    Attributes:
        is_skippable (bool): The final answer.
        _optional_sects (arr): Optional sections bounded by vital sections.
        _optional_sects_len (int): Optional sections count.
    """

    def __init__(self, optional_sects: list[OptionalSect], argv: list[str]) -> None:
        super().__init__(argv)
        self._optional_sects = optional_sects
        self._optional_sects_len = len(optional_sects)

    def _set_argv(self, argv: list[str]) -> _OptionAssignmentResult:
        self._arg_idx = 0
        self._argv = argv
        self._argc = len(argv)

        # Can the inteval be a prefix for any optionals?
        assignmentResult = _IS_INVALID_VALUE
        for optional_sect_idx in range(self._optional_sects_len):
            
            status = self._match(optional_sect_idx, argv)
            if status == _IS_SKIPPABLE_VALUE:
                assignmentResult = _IS_SKIPPABLE_VALUE
            elif status == _IS_COMPLETE_VALUE:
                return _IS_COMPLETE_VALUE
            
        return assignmentResult
            
    def _match(self, section_idx: int, subinterval: list[str]) -> _OptionAssignmentResult:
        """
        Parameters:
        Returns:
        :param self: Description
        :param section_idx: Description
        :type section_idx: int
        :param subinterval: Description
        :type subinterval: list[str]
        :return: Description
        :rtype: list[int]
        """
        if section_idx >= self._optional_sects_len:
            return _IS_INVALID_VALUE
        
        section = self._optional_sects[section_idx]
        if self._dispatch_node(section) == _IS_INVALID_VALUE:
            return _IS_INVALID_VALUE
        
        # Was matched by the current section.
        # Can the rest of the interval be matched to the next sections?
        assignmentResult = _IS_INVALID_VALUE
        for next_idx in range(section_idx + 1, self._optional_sects_len - 1):
            
            start_idx = self._arg_idx
            status = self._match(next_idx, subinterval[self._arg_idx:])
            if status == _IS_SKIPPABLE_VALUE:
                assignmentResult = _IS_SKIPPABLE_VALUE
            elif status == _IS_COMPLETE_VALUE:
                return _IS_COMPLETE_VALUE
            
            # Backtrack step
            self._arg_idx = start_idx

        return assignmentResult

    def _dispatch_node(self, node: OptionalSect | Argument) -> _OptionAssignmentResult:
        if isinstance(node, OptionalSect):
            return self._dispatch_optional_sect(node)
        
        assert isinstance(node, Argument)
        status = self._process_leaf(node)
        if status == False:
            return _IS_INVALID_VALUE
        return _IS_SKIPPABLE_VALUE
    
    def _dispatch_optional_sect(self, node: OptionalSect) -> _OptionAssignmentResult:
        if isinstance(node, OptSet):
            return self._traverse_opt_set(node)
        
        if isinstance(node, Opts):
            return self._traverse_opts(node)
        
        if isinstance(node, Variadic):
            return self._traverse_variadic(node)
        
        assert isinstance(node, KeyedVariadic)
        return self._traverse_keyed_variadic(node)
    
    def _traverse_opt_set(self, node: OptSet) -> _OptionAssignmentResult:
        """
        Validates a set of independent keyed options (order irrelevant).
        Continues consuming as long as the current token matches ANY key in the set.
        """
        assignmentResult = _IS_INVALID_VALUE
        
        start_idx = self._arg_idx
        for pattern in node.patterns:
            
            status = self._dispatch_node(pattern)
            if status == _IS_COMPLETE_VALUE:
                return _IS_COMPLETE_VALUE
            if status == _IS_SKIPPABLE_VALUE:
                assignmentResult = _IS_SKIPPABLE_VALUE
            self._arg_idx = start_idx
        
        return assignmentResult

    def _traverse_opts(self, node: Opts) -> _OptionAssignmentResult:
        """
        Validates a sequence of optional patterns. 
        Backtracks if the full sequence implies a mismatch.
        """
        start_idx = self._arg_idx
        for pattern in node.patterns:
            if self._arg_idx >= self._argc:
                return _IS_SKIPPABLE_VALUE
            
            if self._dispatch_node(pattern) == _IS_INVALID_VALUE:
                self._arg_idx = start_idx
                return _IS_INVALID_VALUE
        
        return _IS_COMPLETE_VALUE

    def _traverse_variadic(self, node: Variadic) -> _OptionAssignmentResult:
        """
        Greedily validates a repeating sequence of patterns (0 or more times).
        """
        one_cycle_match = _IS_INVALID_VALUE

        while _OptionSanitizer._FOREVER:
            start_idx = self._arg_idx
            
            cycle_match = _IS_COMPLETE_VALUE
            for pattern in node.patterns:
                if self._arg_idx >= self._argc:
                    return _IS_SKIPPABLE_VALUE
                
                if self._dispatch_node(pattern) == _IS_INVALID_VALUE:
                    cycle_match = _IS_INVALID_VALUE
                    break
                
            if cycle_match == _IS_INVALID_VALUE:
                self._arg_idx = start_idx
                break
            one_cycle_match = _IS_COMPLETE_VALUE

        return one_cycle_match

    def _traverse_keyed_variadic(self, node: KeyedVariadic) -> _OptionAssignmentResult:
        """
        Greedily validates a repeating sequence of patterns (0 or more times).
        """
        start_idx = self._arg_idx
        if self._arg_idx >= self._argc:
            return _IS_SKIPPABLE_VALUE
        
        if self._dispatch_node(node.key) == _IS_INVALID_VALUE:
            self._arg_idx = start_idx
            return _IS_INVALID_VALUE
        
        return self._traverse_variadic(node)

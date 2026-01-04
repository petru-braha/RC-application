def join_cmd_argv(cmd: str, argv: list[str]) -> str:
    """
    Concatenates a command name and its arguments into a space-separated string.

    Returns:
        str: The formatted command string.

    Raises:
        ValueError: If the command name is empty.
    """
    if not cmd:
        raise ValueError("Command name cannot be empty.")
    
    fragments = [cmd]
    fragments.extend(argv)
    return " ".join(fragments)

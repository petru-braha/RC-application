# Logging files directory

Must exist before running the application. Prevents raising FileNotFoundError.

Log format:

- %(asctime)s - The time the log entry was created.
- %(name)s - The name of the logger.
- %(lineno)d - The line number where the log entry was created.
- %(levelname)s - The severity level of the log entry.
- %(message)s - The log message.

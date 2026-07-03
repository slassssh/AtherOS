"""
AtherOS Tool Errors
"""


class ToolExecutionError(Exception):
    pass


class ToolTimeoutError(ToolExecutionError):
    pass


class ToolValidationError(ToolExecutionError):
    pass
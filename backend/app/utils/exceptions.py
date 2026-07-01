class AtherOSError(Exception):
    """Base exception for AtherOS."""


class PlannerError(AtherOSError):
    pass


class EngineError(AtherOSError):
    pass


class ToolError(AtherOSError):
    pass


class JournalError(AtherOSError):
    pass
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


class LLMError(AtherOSError):
    pass


class DatabaseError(AtherOSError):
    pass


class SecurityError(AtherOSError):
    pass


class PermissionDeniedError(SecurityError):
    pass


class SandboxedExecutionError(ToolError):
    pass


class MemoryError(AtherOSError):
    pass


class SessionError(AtherOSError):
    pass
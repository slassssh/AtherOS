from datetime import datetime, UTC
from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standardized API success response wrapper."""

    success: bool = Field(default=True, description="Indicates call success")
    data: T = Field(description="Payload object")
    message: str = Field(default="Operation completed successfully", description="Status message")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
        description="ISO 8601 UTC timestamp"
    )
    request_id: str = Field(default="", description="Unique request tracking identifier")


class ApiErrorResponse(BaseModel):
    """Standardized API error response wrapper."""

    success: bool = Field(default=False, description="Indicates call failure")
    error_code: str = Field(description="Machine-readable error code")
    message: str = Field(description="Human-readable error summary")
    detail: Optional[Any] = Field(default=None, description="Detailed stack trace or validation errors")
    request_id: str = Field(default="", description="Unique request tracking identifier")


class HealthData(BaseModel):
    """Health check payload."""

    application_status: str = Field(description="Status of the application (e.g. healthy)")
    version: str = Field(description="Application version")
    uptime_seconds: float = Field(description="Server uptime in seconds")
    engine_status: str = Field(description="Engine operational status")
    database_status: str = Field(description="Database connectivity status")


class VersionData(BaseModel):
    """Version payload."""

    app_name: str
    version: str
    environment: str


class ChatRequest(BaseModel):
    """Payload for initiating or continuing chat."""

    message: str = Field(description="User text prompt or command", min_length=1)
    session_id: Optional[str] = Field(default=None, description="Optional existing session UUID")


class ChatData(BaseModel):
    """Response payload for chat."""

    session_id: str
    response: str
    status: str


class GoalRequest(BaseModel):
    """Payload for goal execution."""

    goal: str = Field(description="High level goal description", min_length=1)
    session_id: Optional[str] = Field(default=None, description="Optional target session UUID")


class GoalData(BaseModel):
    """Response payload for goal execution."""

    session_id: str
    goal: str
    status: str
    tasks: List[Any]
    event_count: int


class SessionData(BaseModel):
    """Session info payload."""

    session_id: str
    title: str
    description: str
    state: str
    created_at: str
    updated_at: str


class TaskData(BaseModel):
    """Task detail payload."""

    task_id: str
    description: str
    tool_name: Optional[str] = None
    status: str
    output: Optional[Any] = None
    error: Optional[str] = None
    execution_time: float = 0.0

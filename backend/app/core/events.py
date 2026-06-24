"""
AtherOS Core Events

Defines the shared event types and data structures
used throughout the orchestration engine.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4


class EventType(Enum):
    """
    Represents all event categories
    produced inside the orchestration engine.
    """

    SESSION_CREATED = "SESSION_CREATED"
    USER_MESSAGE_RECEIVED = "USER_MESSAGE_RECEIVED"

    PLAN_CREATED = "PLAN_CREATED"
    PLAN_UPDATED = "PLAN_UPDATED"

    TASK_STARTED = "TASK_STARTED"
    TASK_COMPLETED = "TASK_COMPLETED"
    TASK_FAILED = "TASK_FAILED"

    MEMORY_READ = "MEMORY_READ"
    MEMORY_WRITE = "MEMORY_WRITE"

    RESPONSE_GENERATED = "RESPONSE_GENERATED"

    STATE_CHANGED = "STATE_CHANGED"

    SESSION_COMPLETED = "SESSION_COMPLETED"

    ERROR_OCCURRED = "ERROR_OCCURRED"


class SessionState(Enum):
    """
    Represents the lifecycle state
    of a session.
    """

    INIT = "INIT"
    WAITING_FOR_INPUT = "WAITING_FOR_INPUT"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    GENERATING_RESPONSE = "GENERATING_RESPONSE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ActorType(Enum):
    """
    Identifies who produced an event.
    """

    USER = "USER"
    SYSTEM = "SYSTEM"
    ENGINE = "ENGINE"
    PLANNER = "PLANNER"
    MEMORY = "MEMORY"
    TOOL = "TOOL"


class Priority(Enum):
    """
    Priority level of an event.
    """

    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class JournalEvent:
    """
    Represents a single event
    stored inside the Unified Journal.
    """

    session_id: UUID
    sequence_number: int

    event_type: EventType
    actor: ActorType

    payload: dict[str, Any]

    priority: Priority = Priority.NORMAL

    event_id: UUID = field(default_factory=uuid4)

    created_at: datetime = field(default_factory=datetime.utcnow)
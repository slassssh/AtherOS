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

    session_id: UUID | str
    sequence_number: int

    event_type: EventType
    actor: ActorType

    payload: dict[str, Any]

    priority: Priority = Priority.NORMAL

    event_id: UUID = field(default_factory=uuid4)

    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": str(self.event_id),
            "session_id": str(self.session_id) if self.session_id else None,
            "sequence_number": self.sequence_number,
            "event_type": self.event_type.value if isinstance(self.event_type, EventType) else str(self.event_type),
            "actor": self.actor.value if isinstance(self.actor, ActorType) else str(self.actor),
            "priority": self.priority.value if isinstance(self.priority, Priority) else str(self.priority),
            "payload": self.payload,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "JournalEvent":
        return cls(
            event_id=UUID(data["event_id"]) if isinstance(data.get("event_id"), str) else data.get("event_id", uuid4()),
            session_id=UUID(data["session_id"]) if isinstance(data.get("session_id"), str) else data.get("session_id"),
            sequence_number=data.get("sequence_number", 0),
            event_type=EventType(data["event_type"]) if isinstance(data.get("event_type"), str) and data["event_type"] in EventType.__members__ else EventType.STATE_CHANGED,
            actor=ActorType(data["actor"]) if isinstance(data.get("actor"), str) and data["actor"] in ActorType.__members__ else ActorType.ENGINE,
            priority=Priority(data["priority"]) if isinstance(data.get("priority"), str) and data["priority"] in Priority.__members__ else Priority.NORMAL,
            payload=data.get("payload", {}),
            created_at=datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else datetime.utcnow(),
        )
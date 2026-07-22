from dataclasses import dataclass, field
from datetime import datetime, UTC
from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4


class SystemEventType(str, Enum):
    GOAL_CREATED = "GOAL_CREATED"
    GOAL_STARTED = "GOAL_STARTED"
    GOAL_COMPLETED = "GOAL_COMPLETED"

    TASK_CREATED = "TASK_CREATED"
    TASK_COMPLETED = "TASK_COMPLETED"
    TASK_FAILED = "TASK_FAILED"

    MEMORY_CREATED = "MEMORY_CREATED"
    MEMORY_UPDATED = "MEMORY_UPDATED"

    GRAPH_UPDATED = "GRAPH_UPDATED"

    AGENT_STARTED = "AGENT_STARTED"
    AGENT_FINISHED = "AGENT_FINISHED"

    SECURITY_ALERT = "SECURITY_ALERT"
    PLUGIN_INSTALLED = "PLUGIN_INSTALLED"

    SYSTEM_WARNING = "SYSTEM_WARNING"
    SYSTEM_ERROR = "SYSTEM_ERROR"
    SYSTEM_READY = "SYSTEM_READY"


@dataclass(frozen=True)
class SystemEvent:
    """
    Immutable System Event dataclass.
    Forms the core message envelope for the AtherOS Event Bus.
    """

    source: str
    type: SystemEventType
    payload: Dict[str, Any] = field(default_factory=dict)
    priority: int = 5
    correlation_id: Optional[str] = None
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat() if hasattr(self.timestamp, "isoformat") else str(self.timestamp),
            "source": self.source,
            "type": self.type.value if hasattr(self.type, "value") else str(self.type),
            "payload": self.payload,
            "priority": self.priority,
            "correlation_id": self.correlation_id,
        }

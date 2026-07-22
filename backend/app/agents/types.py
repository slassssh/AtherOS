from dataclasses import dataclass, field
from datetime import datetime, UTC
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class AgentStatus(str, Enum):
    IDLE = "IDLE"
    BUSY = "BUSY"
    FAILED = "FAILED"
    OFFLINE = "OFFLINE"


@dataclass
class AgentTask:
    task_id: str = field(default_factory=lambda: str(uuid4()))
    description: str = ""
    goal: str = ""
    session_id: Optional[str] = None
    input_data: Dict[str, Any] = field(default_factory=dict)
    priority: int = 5
    timeout: int = 30


@dataclass
class AgentResult:
    task_id: str
    agent_id: str
    success: bool
    output: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentMessage:
    source_agent: str
    target_agent: str
    task_id: str
    payload: Dict[str, Any]
    priority: int = 5
    status: str = "PENDING"
    message_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "source_agent": self.source_agent,
            "target_agent": self.target_agent,
            "task_id": self.task_id,
            "priority": self.priority,
            "payload": self.payload,
            "status": self.status,
            "timestamp": self.timestamp.isoformat()
        }

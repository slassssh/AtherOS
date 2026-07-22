from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict
from uuid import UUID, uuid4


class TaskStatus(Enum):
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass
class Task:
    description: str

    task_id: UUID = field(default_factory=uuid4)

    status: TaskStatus = TaskStatus.PENDING
    depends_on: list[UUID] = field(default_factory=list)

    tool: str | None = None
    tool_input: Dict[str, Any] = field(default_factory=dict)
    output: Any = None

    retry_count: int = 0
    max_retries: int = 3

    error: str | None = None
    execution_time: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """
        Return structured task execution dictionary.
        """
        return {
            "task_id": str(self.task_id),
            "description": self.description,
            "tool_name": self.tool,
            "tool_input": self.tool_input,
            "status": self.status.value if isinstance(self.status, TaskStatus) else str(self.status),
            "output": self.output,
            "error": self.error,
            "execution_time": round(self.execution_time, 4),
        }
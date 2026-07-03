from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID, uuid4
from enum import Enum


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
    retry_count: int = 0

    max_retries: int = 3

    error: str | None = None
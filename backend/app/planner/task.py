from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID, uuid4


class TaskStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class Task:
    description: str

    task_id: UUID = field(default_factory=uuid4)

    status: TaskStatus = TaskStatus.PENDING

    depends_on: list[UUID] = field(default_factory=list)

    tool: str | None = None
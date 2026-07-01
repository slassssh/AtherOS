from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import UUID, uuid4

from backend.app.planner.task import Task


@dataclass
class Plan:
    goal: str

    tasks: list[Task] = field(default_factory=list)

    plan_id: UUID = field(default_factory=uuid4)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
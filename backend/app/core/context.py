from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime
from typing import Any


@dataclass
class ExecutionContext:

    session_id: UUID

    variables: dict[str, Any] = field(default_factory=dict)

    current_task: str | None = None

    started_at: datetime = field(default_factory=datetime.utcnow)


    def set(self, key: str, value: Any):

        self.variables[key] = value


    def get(self, key: str):

        return self.variables.get(key)


    def update_task(self, task_id: str):

        self.current_task = task_id
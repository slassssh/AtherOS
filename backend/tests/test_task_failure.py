import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.planner.task import Task, TaskStatus


task = Task(
    description="Broken task"
)


task.retry_count += 1

task.error = "Something failed"


if task.retry_count >= task.max_retries:
    task.status = TaskStatus.FAILED


print(task.retry_count)

print(task.error)

print(task.status)
import sys
from pathlib import Path
from uuid import uuid4

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.core.context import ExecutionContext


context = ExecutionContext(
    session_id=uuid4()
)

context.set(
    "goal",
    "Build AtherOS"
)

context.update_task(
    "task_1"
)


print(context.get("goal"))

print(context.current_task)
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.core.engine import Engine
from backend.app.planner.planner import Planner
from backend.app.planner.task import TaskStatus

planner = Planner()
engine = Engine()

plan = planner.create_plan(
    "Research AI, summarize, create presentation, email"
)

print("Initial Ready Tasks:")

for task in engine.get_ready_tasks(plan):
    print("-", task.description)

engine.execute_task(plan.tasks[0])
print("\nAfter Completing First Task:")

for task in engine.get_ready_tasks(plan):
    print("-", task.description)
    print("\nJournal Events:", engine.journal.event_count())
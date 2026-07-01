import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.planner.planner import Planner

planner = Planner()

plan = planner.create_plan(
    "Research AI Operating Systems, summarize the findings, create a PowerPoint and email it"
)

print(plan.goal)
print()

for i, task in enumerate(plan.tasks, start=1):
    print(f"{i}. {task.description}")
    print(f"   Depends On: {len(task.depends_on)}")
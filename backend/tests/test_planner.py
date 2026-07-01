import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.planner.planner import Planner

planner = Planner()

plan = planner.create_plan(
    "Research AI Operating Systems"
)

print(plan.goal)

print(len(plan.tasks))

print(plan.tasks[0].description)
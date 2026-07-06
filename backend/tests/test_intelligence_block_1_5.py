import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.intelligence.reasoning import ReasoningEngine
from backend.app.intelligence.decision import DecisionEngine
from backend.app.intelligence.goal import GoalAnalyzer
from backend.app.intelligence.decomposer import TaskDecomposer
from backend.app.intelligence.execution_planner import ExecutionPlanner


reason = ReasoningEngine()

decision = DecisionEngine()

goal = GoalAnalyzer()

decomposer = TaskDecomposer()

planner = ExecutionPlanner()


analysis = goal.analyze(
    "Build AtherOS Intelligence"
)


tasks = decomposer.decompose(
    analysis["goal"]
)


plan = planner.plan(
    tasks
)


print(
    reason.reason(
        "Phase 6"
    )
)


print(
    decision.decide(
        [
            "continue",
            "stop"
        ]
    )
)


print(plan)
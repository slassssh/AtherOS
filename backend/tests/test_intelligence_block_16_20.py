import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.intelligence.memory_reasoning import MemoryAwareReasoning
from backend.app.intelligence.context_planner import ContextPlanner
from backend.app.intelligence.priority import DynamicPriority
from backend.app.intelligence.multi_step import MultiStepExecution
from backend.app.intelligence.failure_recovery import FailureRecovery


memory_ai = MemoryAwareReasoning()

planner = ContextPlanner()

priority = DynamicPriority()

executor = MultiStepExecution()

recovery = FailureRecovery()


print(
    memory_ai.think(
        "Phase 5 complete",
        "Build Phase 6"
    )
)


steps = planner.plan(
    "AtherOS"
)


print(
    priority.prioritize(
        [
            "low",
            "high"
        ]
    )
)


print(
    executor.execute(
        steps
    )
)


print(
    recovery.recover(
        "Tool failed"
    )
)
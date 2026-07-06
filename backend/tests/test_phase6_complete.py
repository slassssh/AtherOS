import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.intelligence.controller import AgentController
from backend.app.intelligence.agent_logs import AgentLogs
from backend.app.intelligence.agent_metrics import AgentMetrics
from backend.app.intelligence.safety import AgentSafety
from backend.app.intelligence.reasoning import ReasoningEngine


controller = AgentController()

logs = AgentLogs()

metrics = AgentMetrics()

safety = AgentSafety()

reason = ReasoningEngine()


if safety.allow(
    "execute"
):

    result = controller.execute(
        "Build autonomous AI"
    )


    thought = reason.reason(
        result["goal"]
    )


    logs.add(
        thought
    )


    metrics.record(
        True
    )


print(
    logs.all()
)


print(
    metrics.stats()
)
import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.intelligence.agent_state import AgentState
from backend.app.intelligence.runtime import AgentRuntime
from backend.app.intelligence.autonomous_loop import AutonomousLoop
from backend.app.intelligence.action_selector import ActionSelector
from backend.app.intelligence.tool_selector import ToolSelector


state = AgentState()

runtime = AgentRuntime()

loop = AutonomousLoop()

selector = ActionSelector()

tool_ai = ToolSelector()


state.update(
    "running"
)


print(
    state.get()
)


print(
    runtime.run(
        "Analyze project"
    )
)


print(
    loop.cycle()
)


print(
    selector.select(
        [
            "execute",
            "wait"
        ]
    )
)


print(
    tool_ai.select_tool(
        "write code"
    )
)
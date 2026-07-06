import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.memory.tool_memory import ToolMemory


memory = ToolMemory()


memory.remember_tool(
    "python",
    {
        "runs": 10,
        "status": "healthy"
    }
)


tool = memory.recall_tool(
    "python"
)


print(
    tool["runs"]
)


print(
    tool["status"]
)
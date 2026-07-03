import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


from backend.app.core.tool_executor import ToolExecutor
from backend.app.tools.registry import ToolRegistry
from backend.app.tools.python_tool import PythonTool


registry = ToolRegistry()

registry.register(
    PythonTool()
)


executor = ToolExecutor(
    registry
)


result = executor.execute(
    "python"
)


print(result)
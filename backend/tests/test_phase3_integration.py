import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


from backend.app.tools.registry import ToolRegistry
from backend.app.tools.python_tool import PythonTool

from backend.app.core.tool_executor import ToolExecutor


registry = ToolRegistry()


registry.register(
    PythonTool()
)


executor = ToolExecutor(
    registry
)


result = executor.execute(
    "python",
    code="print('Phase 3 Complete')"
)


metrics = registry.get_metrics(
    "python"
)


if result.success:
    metrics.record_success()

else:
    metrics.record_failure()


print(result)

print(metrics)

print(
    registry.list_tools()
)
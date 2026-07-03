import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


from backend.app.tools.registry import ToolRegistry
from backend.app.tools.python_tool import PythonTool


registry = ToolRegistry()

registry.register(
    PythonTool()
)


metrics = registry.get_metrics(
    "python"
)


metrics.record_success()

metrics.record_failure()


print(metrics)
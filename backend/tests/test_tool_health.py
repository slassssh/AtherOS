import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.tools.health import ToolHealth
from backend.app.tools.python_tool import PythonTool


health = ToolHealth()

tool = PythonTool()


print(
    health.check(
        tool
    )
)
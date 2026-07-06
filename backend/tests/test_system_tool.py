import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.tools.system_tool import SystemTool


tool = SystemTool()


result = tool.execute(
    action="stats"
)


print(result)
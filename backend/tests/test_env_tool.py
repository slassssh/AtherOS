import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.tools.env_tool import EnvironmentTool


tool = EnvironmentTool()


print(
    tool.execute(
        action="get",
        key="USERNAME"
    )
)
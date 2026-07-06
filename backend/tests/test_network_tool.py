import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.tools.network_tool import NetworkTool


tool = NetworkTool()


print(
    tool.execute(
        action="hostname"
    )
)


print(
    tool.execute(
        action="ip"
    )
)
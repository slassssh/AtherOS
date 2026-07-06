import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.tools.config_tool import ConfigTool


tool = ConfigTool()


print(
    tool.execute(
        action="write",
        path="atheros_config.json",
        data={
            "version": "0.4",
            "phase": "tools"
        }
    )
)


print(
    tool.execute(
        action="read",
        path="atheros_config.json"
    )
)
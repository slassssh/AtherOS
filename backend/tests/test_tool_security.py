import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.tools.security import ToolSecurity
from backend.app.tools.python_tool import PythonTool
from backend.app.tools.permissions import ToolPermission


tool = PythonTool()


security = ToolSecurity(
    allowed_permissions=[
        ToolPermission.CODE_EXECUTION
    ]
)


print(
    security.check(
        tool
    )
)
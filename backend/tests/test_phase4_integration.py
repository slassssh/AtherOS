import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.tools.registry import ToolRegistry
from backend.app.tools.system_tool import SystemTool
from backend.app.tools.security import ToolSecurity
from backend.app.tools.permissions import ToolPermission

from backend.app.tools.history import (
    ToolHistory,
    ToolHistoryItem
)

from backend.app.core.tool_executor import ToolExecutor


registry = ToolRegistry()


system_tool = SystemTool()


registry.register(
    system_tool
)


security = ToolSecurity(
    allowed_permissions=[
        ToolPermission.SYSTEM_ACCESS
    ]
)


history = ToolHistory()


if security.check(
    system_tool
):

    executor = ToolExecutor(
        registry
    )


    result = executor.execute(
        "system",
        action="stats"
    )


    history.add(
        ToolHistoryItem(
            tool="system",
            success=result.success
        )
    )


    print(result)

    print(history.all())


else:

    print(
        "Permission denied"
    )
import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.tools.discovery import ToolDiscovery
from backend.app.tools.health import ToolHealth
from backend.app.tools.sandbox import ToolSandbox
from backend.app.tools.audit import (
    AuditTrail,
    AuditRecord
)

from backend.app.tools.registry import ToolRegistry
from backend.app.tools.system_tool import SystemTool

from backend.app.core.tool_executor import ToolExecutor


discovery = ToolDiscovery()

health = ToolHealth()

sandbox = ToolSandbox()

audit = AuditTrail()

registry = ToolRegistry()


tools = discovery.discover(
    [
        SystemTool()
    ]
)


for tool in tools:


    if (
        health.check(tool)
        and
        sandbox.allowed(
            tool.metadata.name
        )
    ):


        registry.register(
            tool
        )


executor = ToolExecutor(
    registry
)


result = executor.execute(
    "system",
    action="stats"
)


audit.record(
    AuditRecord(
        actor="AtherOS",
        action="phase4_test",
        details=result.success
    )
)


print(result)

print(
    audit.get_records()
)

print(
    registry.list_tools()
)
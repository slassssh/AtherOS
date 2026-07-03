import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


from backend.app.tools.base import BaseTool
from backend.app.tools.registry import ToolRegistry
from backend.app.tools.result import ToolResult
from backend.app.tools.metadata import ToolMetadata


class DummyTool(BaseTool):
    metadata = ToolMetadata(
        name="dummy",
        description="Testing tool",
        category="test",
    )


    def execute(self, **kwargs):

        return ToolResult(
            success=True,
            output="Hello AtherOS"
        )


registry = ToolRegistry()

tool = DummyTool()


registry.register(tool)


print(
    registry.list_tools()
)


result = registry.get_tool(
    "dummy"
).execute()


print(result)
"""
AtherOS Tool Executor

Bridge between Engine and Tool Registry.
"""


from backend.app.tools.registry import ToolRegistry
from backend.app.tools.result import ToolResult


class ToolExecutor:

    def __init__(
        self,
        registry: ToolRegistry
    ):

        self.registry = registry


    def execute(
        self,
        tool_name: str,
        **kwargs
    ) -> ToolResult:


        tool = self.registry.get_tool(
            tool_name
        )


        if tool is None:

            return ToolResult(
                success=False,
                error="Tool not found"
            )

        if tool.schema:

            valid, missing = tool.schema.validate(
                kwargs
            )

            if not valid:

                return ToolResult(
                    success=False,
                    error=f"Missing fields: {missing}"
                )


        return tool.execute(
            **kwargs
        )
from abc import ABC, abstractmethod
from typing import Optional

from backend.app.tools.registry import ToolRegistry
from backend.app.tools.result import ToolResult


class BaseToolExecutor(ABC):
    """
    Abstract interface for tool executors in AtherOS.
    Ensures Engine calls tools only through an abstract gateway.
    """

    @abstractmethod
    def execute(self, tool_name: str, **kwargs) -> ToolResult:
        """
        Execute a tool by name with arguments.
        """
        pass


class ToolExecutor(BaseToolExecutor):
    """
    Single execution gateway for tool execution.
    Inspects tool registry, validates parameters, and executes tools safely.
    """

    def __init__(self, registry: Optional[ToolRegistry] = None):
        self.registry = registry if registry is not None else ToolRegistry()

    def execute(
        self,
        tool_name: str,
        **kwargs
    ) -> ToolResult:
        if not tool_name:
            return ToolResult(
                success=True,
                output="No tool required for task execution."
            )

        tool = self.registry.get_tool(tool_name)

        if tool is None:
            return ToolResult(
                success=False,
                error=f"Tool '{tool_name}' not found in registry."
            )

        try:
            if hasattr(tool, "schema") and tool.schema:
                valid, missing = tool.schema.validate(kwargs)
                if not valid:
                    return ToolResult(
                        success=False,
                        error=f"Tool parameter validation failed. Missing fields: {missing}"
                    )

            return tool.execute(**kwargs)

        except Exception as error:
            return ToolResult(
                success=False,
                error=f"Tool execution exception in '{tool_name}': {str(error)}"
            )
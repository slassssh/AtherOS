"""
AtherOS Tool Registry

Stores and manages available tools.
"""


from backend.app.tools.base import BaseTool
from backend.app.tools.metrics import ToolMetrics

class ToolRegistry:

    def __init__(self):

        self.tools = {}
        self.metrics = {}

    def register(
        self,
        tool: BaseTool
    ):

        self.tools[
            tool.metadata.name
        ] = tool
        self.metrics[tool.metadata.name] = ToolMetrics()

    def get_tool(
        self,
        name: str
    ):

        return self.tools.get(
            name
        )


    def list_tools(self):

        return list(
            self.tools.keys()
        )

    def get_metrics(
        self,
        tool_name: str
    ):

        return self.metrics.get(
            tool_name
        )
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
        self._register_defaults()

    def _register_defaults(self):
        try:
            from backend.app.tools.file_tool import FileTool
            from backend.app.tools.python_tool import PythonTool
            from backend.app.tools.terminal_tool import TerminalTool
            for tool_cls in (FileTool, PythonTool, TerminalTool):
                tool = tool_cls()
                self.register(tool)
        except Exception:
            pass

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
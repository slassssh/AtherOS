"""
AtherOS Python Tool

Executes Python code snippets.
"""


from typing import Optional

from backend.app.tools.base import BaseTool
from backend.app.tools.metadata import ToolMetadata
from backend.app.tools.permissions import ToolPermission
from backend.app.tools.result import ToolResult
from backend.app.tools.sandbox import ToolSandbox
from backend.app.tools.schema import ToolSchema


class PythonTool(BaseTool):

    metadata = ToolMetadata(
        name="python",
        description="Execute Python code snippets inside an isolated sandbox",
        category="execution",
        permissions=[
            ToolPermission.RUN_PYTHON
        ]
    )

    schema = ToolSchema(
        required=[
            "code"
        ]
    )

    def __init__(self, sandbox: Optional[ToolSandbox] = None):
        self.sandbox = sandbox or ToolSandbox()

    def execute(
        self,
        code: str,
        session_id: Optional[str] = None,
        **kwargs
    ) -> ToolResult:
        """
        Executes Python code via the hardened ToolSandbox subprocess runner.
        No raw in-process exec() is permitted.
        """
        return self.sandbox.execute_python_code(code, session_id=session_id)
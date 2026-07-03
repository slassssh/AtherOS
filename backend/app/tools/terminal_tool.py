"""
AtherOS Terminal Tool

Executes system commands safely.
"""


import subprocess

from backend.app.tools.base import BaseTool
from backend.app.tools.result import ToolResult
from backend.app.tools.metadata import ToolMetadata
from backend.app.tools.permissions import ToolPermission

class TerminalTool(BaseTool):
    metadata = ToolMetadata(
        name="terminal",
        description="Execute terminal commands",
        category="system",
        permissions=[
            ToolPermission.SYSTEM_ACCESS
        ]
    )

    def execute(
        self,
        command: str
    ) -> ToolResult:


        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                shell=True,
                timeout=10
            )

            if result.returncode == 0:

                return ToolResult(
                    success=True,
                    output=result.stdout
                )


            return ToolResult(
                success=False,
                error=result.stderr
            )

        except subprocess.TimeoutExpired:

            return ToolResult(
                success=False,
                error="Command timed out"
            )
        except Exception as error:
            return ToolResult(
                success=False,
                error=str(error)
            )
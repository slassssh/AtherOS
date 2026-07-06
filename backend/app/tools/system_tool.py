"""
AtherOS System Tool

Monitors system resources.
"""


import psutil


from backend.app.tools.base import BaseTool
from backend.app.tools.result import ToolResult
from backend.app.tools.metadata import ToolMetadata
from backend.app.tools.permissions import ToolPermission
from backend.app.tools.schema import ToolSchema


class SystemTool(BaseTool):

    metadata = ToolMetadata(
        name="system",
        description="Monitor system resources",
        category="system",
        permissions=[
            ToolPermission.SYSTEM_ACCESS
        ]
    )


    schema = ToolSchema(
        required=[
            "action"
        ]
    )


    def execute(
        self,
        action: str
    ) -> ToolResult:


        try:


            if action == "stats":

                return ToolResult(
                    True,
                    {
                        "cpu": psutil.cpu_percent(),

                        "memory": psutil.virtual_memory().percent,

                        "disk": psutil.disk_usage("/").percent
                    }
                )


            return ToolResult(
                False,
                error="Unknown action"
            )


        except Exception as error:

            return ToolResult(
                False,
                error=str(error)
            )
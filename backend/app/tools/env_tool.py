"""
AtherOS Environment Tool

Reads environment variables.
"""


import os


from backend.app.tools.base import BaseTool
from backend.app.tools.result import ToolResult
from backend.app.tools.metadata import ToolMetadata
from backend.app.tools.permissions import ToolPermission
from backend.app.tools.schema import ToolSchema


class EnvironmentTool(BaseTool):

    metadata = ToolMetadata(
        name="environment",
        description="Manage environment variables",
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
        action: str,
        key: str | None = None
    ) -> ToolResult:


        try:


            if action == "get":

                return ToolResult(
                    True,
                    os.getenv(
                        key
                    )
                )


            if action == "list":

                return ToolResult(
                    True,
                    dict(os.environ)
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
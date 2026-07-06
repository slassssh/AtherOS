"""
AtherOS Package Tool

Handles package information.
"""


import subprocess


from backend.app.tools.base import BaseTool
from backend.app.tools.result import ToolResult
from backend.app.tools.metadata import ToolMetadata
from backend.app.tools.permissions import ToolPermission
from backend.app.tools.schema import ToolSchema


class PackageTool(BaseTool):

    metadata = ToolMetadata(
        name="package",
        description="Package manager operations",
        category="development",
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


            if action == "list":

                result = subprocess.run(
                    [
                        "pip",
                        "list"
                    ],
                    capture_output=True,
                    text=True
                )


                return ToolResult(
                    True,
                    result.stdout
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
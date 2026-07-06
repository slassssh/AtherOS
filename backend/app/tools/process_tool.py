"""
AtherOS Process Tool

Inspects running system processes.
"""


import psutil


from backend.app.tools.base import BaseTool
from backend.app.tools.result import ToolResult
from backend.app.tools.metadata import ToolMetadata
from backend.app.tools.permissions import ToolPermission
from backend.app.tools.schema import ToolSchema


class ProcessTool(BaseTool):

    metadata = ToolMetadata(
        name="process",
        description="Inspect running processes",
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


            if action == "list":

                processes = []


                for process in psutil.process_iter(
                    [
                        "pid",
                        "name"
                    ]
                ):


                    processes.append(
                        process.info
                    )


                return ToolResult(
                    True,
                    processes[:10]
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
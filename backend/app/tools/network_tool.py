"""
AtherOS Network Tool

Checks network connectivity.
"""


import socket


from backend.app.tools.base import BaseTool
from backend.app.tools.result import ToolResult
from backend.app.tools.metadata import ToolMetadata
from backend.app.tools.permissions import ToolPermission
from backend.app.tools.schema import ToolSchema


class NetworkTool(BaseTool):

    metadata = ToolMetadata(
        name="network",
        description="Network diagnostics",
        category="network",
        permissions=[
            ToolPermission.NETWORK_ACCESS
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


            if action == "hostname":

                return ToolResult(
                    True,
                    socket.gethostname()
                )


            if action == "ip":

                hostname = socket.gethostname()


                return ToolResult(
                    True,
                    socket.gethostbyname(
                        hostname
                    )
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
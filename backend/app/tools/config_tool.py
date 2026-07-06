"""
AtherOS Config Tool

Manages JSON configuration files.
"""


import json
from pathlib import Path


from backend.app.tools.base import BaseTool
from backend.app.tools.result import ToolResult
from backend.app.tools.metadata import ToolMetadata
from backend.app.tools.permissions import ToolPermission
from backend.app.tools.schema import ToolSchema


class ConfigTool(BaseTool):

    metadata = ToolMetadata(
        name="config",
        description="Manage configuration files",
        category="configuration",
        permissions=[
            ToolPermission.FILE_ACCESS
        ]
    )


    schema = ToolSchema(
        required=[
            "action",
            "path"
        ]
    )


    def execute(
        self,
        action: str,
        path: str,
        **kwargs
    ) -> ToolResult:


        try:

            config_path = Path(path)


            if action == "read":

                data = json.loads(
                    config_path.read_text()
                )


                return ToolResult(
                    True,
                    data
                )


            if action == "write":

                config_path.write_text(
                    json.dumps(
                        kwargs.get(
                            "data",
                            {}
                        ),
                        indent=4
                    )
                )


                return ToolResult(
                    True,
                    "Config saved"
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
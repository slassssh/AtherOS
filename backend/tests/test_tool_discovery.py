import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.tools.discovery import ToolDiscovery
from backend.app.tools.python_tool import PythonTool
from backend.app.tools.file_tool import FileTool


discovery = ToolDiscovery()


tools = discovery.discover(
    [
        PythonTool(),
        FileTool()
    ]
)


for tool in tools:

    print(
        tool.metadata.name
    )
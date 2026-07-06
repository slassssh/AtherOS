import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.tools.process_tool import ProcessTool


tool = ProcessTool()


result = tool.execute(
    action="list"
)


print(result)
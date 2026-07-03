import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


from backend.app.tools.file_tool import FileTool


tool = FileTool()


write_result = tool.execute(
    action="write",
    path="test.txt",
    content="Hello from AtherOS"
)


print(write_result)


read_result = tool.execute(
    action="read",
    path="test.txt"
)


print(read_result)
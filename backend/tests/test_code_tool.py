import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.tools.code_tool import CodeTool


tool = CodeTool()


print(
    tool.execute(
        action="analyze",
        path="backend/app/tools/code_tool.py"
    )
)


print(
    tool.execute(
        action="append",
        path="test_folder/test.txt",
        content="\nUpdated by Code Tool"
    )
)
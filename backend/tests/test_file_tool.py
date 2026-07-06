import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


from backend.app.tools.file_tool import FileTool


tool = FileTool()


print(
    tool.execute(
        action="mkdir",
        path="test_folder"
    )
)


print(
    tool.execute(
        action="write",
        path="test_folder/test.txt",
        content="AtherOS Phase 4"
    )
)


print(
    tool.execute(
        action="read",
        path="test_folder/test.txt"
    )
)


print(
    tool.execute(
        action="list",
        path="test_folder"
    )
)
print(
    tool.execute(
        action="search",
        path="test_folder",
        pattern="*.txt"
    )
)
import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.tools.package_tool import PackageTool


tool = PackageTool()


result = tool.execute(
    action="list"
)


print(
    result.success
)

print(
    result.output[:100]
)
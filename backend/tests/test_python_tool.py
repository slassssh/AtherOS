import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


from backend.app.tools.python_tool import PythonTool


tool = PythonTool()


result = tool.execute(
    code="print(10 + 20)"
)


print(result)
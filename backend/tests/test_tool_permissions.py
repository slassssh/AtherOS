import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


from backend.app.tools.python_tool import PythonTool


tool = PythonTool()


print(tool.metadata.name)

print(tool.metadata.category)

print(tool.metadata.permissions)
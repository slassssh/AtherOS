import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


from backend.app.tools.terminal_tool import TerminalTool


tool = TerminalTool()


result = tool.execute(
    command="echo Hello AtherOS"
)


print(result)
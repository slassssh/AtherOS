import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.tools.history import (
    ToolHistory,
    ToolHistoryItem
)


history = ToolHistory()


history.add(
    ToolHistoryItem(
        tool="python",
        success=True
    )
)


history.add(
    ToolHistoryItem(
        tool="terminal",
        success=False
    )
)


for item in history.all():

    print(item)
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.utils.exceptions import (
    AtherOSError,
    PlannerError,
    EngineError,
    ToolError,
    JournalError,
)


exceptions = [
    AtherOSError("Base Error"),
    PlannerError("Planner Error"),
    EngineError("Engine Error"),
    ToolError("Tool Error"),
    JournalError("Journal Error"),
]

for exception in exceptions:
    try:
        raise exception
    except Exception as error:
        print(type(error).__name__, "->", error)
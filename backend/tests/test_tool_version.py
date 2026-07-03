import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


from backend.app.tools.version import ToolVersion


version = ToolVersion(
    "1.2.0"
)


print(
    version.compatible(
        "1.0.0"
    )
)


print(
    version.compatible(
        "2.0.0"
    )
)
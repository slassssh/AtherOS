import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.tools.sandbox import ToolSandbox


sandbox = ToolSandbox()


print(
    sandbox.allowed(
        "python"
    )
)


sandbox.block(
    "terminal"
)


print(
    sandbox.allowed(
        "terminal"
    )
)
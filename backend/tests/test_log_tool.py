import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.tools.log_tool import LogTool


Path("sample.log").write_text(
    """
    INFO Started
    WARNING Low Memory
    ERROR Failed Task
    """
)


tool = LogTool()


print(
    tool.execute(
        action="analyze",
        path="sample.log"
    )
)
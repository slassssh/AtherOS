import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.tools.audit import (
    AuditTrail,
    AuditRecord
)


audit = AuditTrail()


audit.record(
    AuditRecord(
        actor="AtherOS",
        action="execute_tool",
        details={
            "tool": "python"
        }
    )
)


for record in audit.get_records():

    print(record)
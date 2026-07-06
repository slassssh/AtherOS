"""
AtherOS Audit Trail

Tracks detailed tool actions.
"""


from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class AuditRecord:

    actor: str

    action: str

    details: Any

    timestamp: datetime = field(
        default_factory=datetime.now
    )


class AuditTrail:


    def __init__(self):

        self.records = []


    def record(
        self,
        entry: AuditRecord
    ):

        self.records.append(
            entry
        )


    def get_records(
        self
    ):

        return self.records.copy()
"""
AtherOS Tool History

Records tool executions.
"""


from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ToolHistoryItem:

    tool: str

    success: bool

    timestamp: datetime = field(
        default_factory=datetime.now
    )


class ToolHistory:


    def __init__(self):

        self.records = []


    def add(
        self,
        item: ToolHistoryItem
    ):

        self.records.append(
            item
        )


    def all(
        self
    ):

        return self.records.copy()
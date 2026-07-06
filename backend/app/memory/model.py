"""
AtherOS Memory Model

Defines a single memory unit.
"""


from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4, UUID


@dataclass
class Memory:

    content: str

    category: str

    importance: int = 1

    id: UUID = field(
        default_factory=uuid4
    )

    created_at: datetime = field(
        default_factory=datetime.now
    )
# backend/app/core/session.py

"""
AtherOS Session Model

Represents a long-lived project or goal.
A session owns journal events and tracks
the lifecycle of user work.
"""

from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Any
from uuid import UUID, uuid4

from backend.app.core.events import SessionState


@dataclass
class Session:
    """
    Represents a user session/project.
    """

    title: str
    description: str

    state: SessionState = SessionState.INIT

    metadata: dict[str, Any] = field(default_factory=dict)

    session_id: UUID = field(default_factory=uuid4)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
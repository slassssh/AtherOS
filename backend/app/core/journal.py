"""
AtherOS Unified Journal

Stores and retrieves events generated
during a session lifecycle.
"""

from typing import List

from backend.app.core.events import JournalEvent


class Journal:  
    """
    In-memory event journal for Version 0.1.

    Later versions may replace this with
    PostgreSQL-backed persistence.
    """

    def __init__(self) -> None:
        self._events: List[JournalEvent] = []

    def add_event(self, event: JournalEvent) -> None:
        """
        Add an event to the journal.
        """
        self._events.append(event)

    def get_events(self) -> List[JournalEvent]:
        """
        Return all events.
        """
        return self._events.copy()

    def get_last_event(self) -> JournalEvent | None:
        """
        Return the most recent event.
        """
        if not self._events:
            return None

        return self._events[-1]

    def event_count(self) -> int:
        """
        Return total number of events.
        """
        return len(self._events)
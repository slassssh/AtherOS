import json
from typing import List, Optional

from backend.app.core.events import JournalEvent
from backend.app.database.models import JournalEventModel
from backend.app.database.repository import JournalRepository, UnitOfWork


class Journal:  
    """
    Unified Journal for Version 0.1+.
    Stores events in-memory and persists them to SQLite/Relational DB via JournalRepository.
    """

    def __init__(self) -> None:
        self._events: List[JournalEvent] = []

    def add_event(self, event: JournalEvent) -> None:
        """
        Add an event to the journal and persist to database.
        """
        self._events.append(event)
        try:
            with UnitOfWork() as uow:
                repo = JournalRepository(uow.session)
                model = JournalEventModel(
                    id=str(event.event_id),
                    session_id=str(event.session_id) if event.session_id else None,
                    sequence_number=event.sequence_number,
                    event_type=event.event_type.value if hasattr(event.event_type, "value") else str(event.event_type),
                    actor=event.actor.value if hasattr(event.actor, "value") else str(event.actor),
                    priority=event.priority.value if hasattr(event.priority, "value") else str(event.priority),
                    payload_json=json.dumps(event.payload or {}),
                    created_at=event.created_at
                )
                repo.save(model)
        except Exception:
            pass

    def get_events(self) -> List[JournalEvent]:
        """
        Return all events.
        """
        return self._events.copy()

    def get_events_by_session(self, session_id: str | None) -> List[JournalEvent]:
        """
        Return events for a specific session ID.
        """
        if not session_id:
            return self.get_events()
        str_id = str(session_id)
        return [e for e in self._events if str(e.session_id) == str_id]

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

    def clear(self) -> None:
        """
        Clear all in-memory events.
        """
        self._events.clear()
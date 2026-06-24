import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.app.core.events import (
    ActorType,
    EventType,
    JournalEvent,
)
from backend.app.core.journal import Journal

journal = Journal()

event = JournalEvent(
    session_id=None,
    sequence_number=1,
    event_type=EventType.SESSION_CREATED,
    actor=ActorType.SYSTEM,
    payload={"message": "Session started"},
)

journal.add_event(event)

print("Events:", journal.event_count())
print("Last Event:", journal.get_last_event())
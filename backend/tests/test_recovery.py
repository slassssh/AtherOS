import sys
from pathlib import Path
from uuid import uuid4

sys.path.append(str(Path(__file__).resolve().parents[2]))


from backend.app.core.recovery import EngineRecovery
from backend.app.core.journal import Journal
from backend.app.core.events import (
    JournalEvent,
    EventType,
    ActorType
)


journal = Journal()

session_id = uuid4()


journal.add_event(
    JournalEvent(
        session_id=session_id,
        sequence_number=1,
        event_type=EventType.SESSION_CREATED,
        actor=ActorType.SYSTEM,
        payload={
            "goal": "Build AI OS"
        }
    )
)


journal.add_event(
    JournalEvent(
        session_id=session_id,
        sequence_number=2,
        event_type=EventType.TASK_COMPLETED,
        actor=ActorType.ENGINE,
        payload={
            "last_completed": "Planner"
        }
    )
)


recovery = EngineRecovery(journal)

result = recovery.recover()

print(result)
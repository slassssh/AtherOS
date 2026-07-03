import sys
from pathlib import Path
from uuid import uuid4

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.core.replay import ReplayEngine
from backend.app.core.journal import Journal, JournalEvent
from backend.app.core.events import EventType, ActorType


journal = Journal()

session_id = uuid4()


journal.add_event(
    JournalEvent(
        session_id=session_id,
        event_type=EventType.SESSION_CREATED,
        actor=ActorType.SYSTEM,
        sequence_number=1,
        payload={
            "session": "AtherOS Build"
        },
    )
)


journal.add_event(
    JournalEvent(
        session_id=session_id,
        event_type=EventType.TASK_COMPLETED,
        actor=ActorType.ENGINE,
        sequence_number=2,
        payload={
            "last_task": "Planner"
        },
    )
)


replay = ReplayEngine(journal)

state = replay.rebuild_state()

print(state)
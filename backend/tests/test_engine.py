import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.core.engine import Engine
from backend.app.core.events import SessionState

engine = Engine()

session = engine.create_session(
    "AtherOS Development",
    "Building the engine",
)

print(session.state)

success = engine.transition(
    session,
    SessionState.PLANNING,
)

print(success)
print(session.state)

print(
    engine.journal.event_count()
)
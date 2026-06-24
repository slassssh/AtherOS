import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.core.events import SessionState
from backend.app.core.state_machine import StateMachine

print(
    StateMachine.can_transition(
        SessionState.INIT,
        SessionState.PLANNING,
    )
)

print(
    StateMachine.can_transition(
        SessionState.COMPLETED,
        SessionState.PLANNING,
    )
)
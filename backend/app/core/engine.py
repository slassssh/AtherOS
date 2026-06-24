"""
AtherOS Core Engine

Coordinates sessions, journal events,
and state transitions.
"""

from backend.app.core.events import (
    ActorType,
    EventType,
    JournalEvent,
    SessionState,
)

from backend.app.core.journal import Journal
from backend.app.core.session import Session
from backend.app.core.state_machine import StateMachine


class Engine:
    """
    Core orchestration engine.
    """

    def __init__(self) -> None:
        self.journal = Journal()

    def create_session(
        self,
        title: str,
        description: str,
    ) -> Session:

        session = Session(
            title=title,
            description=description,
        )

        event = JournalEvent(
            session_id=session.session_id,
            sequence_number=1,
            event_type=EventType.SESSION_CREATED,
            actor=ActorType.SYSTEM,
            payload={
                "title": title,
            },
        )

        self.journal.add_event(event)

        return session

    def transition(
        self,
        session: Session,
        new_state: SessionState,
    ) -> bool:

        if not StateMachine.can_transition(
            session.state,
            new_state,
        ):
            return False

        session.state = new_state

        event = JournalEvent(
            session_id=session.session_id,
            sequence_number=self.journal.event_count() + 1,
            event_type=EventType.STATE_CHANGED,
            actor=ActorType.ENGINE,
            payload={
                "new_state": new_state.value,
            },
        )

        self.journal.add_event(event)

        return True
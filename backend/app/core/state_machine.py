"""
AtherOS State Machine

Controls valid session state transitions.
"""

from backend.app.core.events import SessionState


class StateMachine:
    """
    Validates state transitions.
    """

    VALID_TRANSITIONS = {
        SessionState.INIT: [
            SessionState.PLANNING,
        ],

        SessionState.PLANNING: [
            SessionState.EXECUTING,
            SessionState.FAILED,
        ],

        SessionState.EXECUTING: [
            SessionState.GENERATING_RESPONSE,
            SessionState.FAILED,
        ],

        SessionState.GENERATING_RESPONSE: [
            SessionState.COMPLETED,
            SessionState.FAILED,
        ],

        SessionState.COMPLETED: [],

        SessionState.FAILED: [],
    }

    @classmethod
    def can_transition(
        cls,
        current_state: SessionState,
        next_state: SessionState,
    ) -> bool:

        allowed_states = cls.VALID_TRANSITIONS.get(
            current_state,
            [],
        )

        return next_state in allowed_states
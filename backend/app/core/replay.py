"""
AtherOS Replay Engine

Rebuilds runtime state from the
append-only journal.
"""


class ReplayEngine:
    """
    Replays journal events to reconstruct
    the latest application state.
    """

    def __init__(self, journal):
        self.journal = journal


    def rebuild_state(self):

        state = {}

        events = self.journal.get_events()

        for event in events:

            state["last_event"] = event.event_type

            if event.payload:
                state.update(event.payload)

        return state
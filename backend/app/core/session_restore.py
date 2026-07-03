"""
AtherOS Session Restore

Restores a previous execution session
from journal history.
"""


from backend.app.core.replay import ReplayEngine


class SessionRestore:

    def __init__(self, journal):
        self.journal = journal


    def restore(self):

        replay = ReplayEngine(
            self.journal
        )

        restored_state = replay.rebuild_state()

        return restored_state
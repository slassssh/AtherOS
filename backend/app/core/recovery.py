"""
AtherOS Engine Recovery

Allows the engine to resume execution
after interruption or shutdown.
"""


from backend.app.core.session_restore import SessionRestore


class EngineRecovery:

    def __init__(self, journal):
        self.journal = journal


    def recover(self):

        restore = SessionRestore(
            self.journal
        )

        state = restore.restore()

        return {
            "recovered": True,
            "state": state
        }
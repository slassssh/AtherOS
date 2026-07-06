from app.runtime.controller import RuntimeController
from app.runtime.metrics import RuntimeMetrics
from app.runtime.runtime_logs import RuntimeLogs
from app.runtime.safety import RuntimeSafety


class RuntimeIntegration:

    def __init__(self):

        self.controller = RuntimeController()
        self.metrics = RuntimeMetrics()
        self.logs = RuntimeLogs()
        self.safety = RuntimeSafety()


    def boot(self):

        self.controller.enable()

        self.metrics.record(
            "boot",
            True
        )

        self.logs.add(
            "runtime booted"
        )

        return {
            "running": self.controller.status(),
            "safe": True
        }
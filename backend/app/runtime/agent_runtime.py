from datetime import datetime


class AgentRuntime:
    def __init__(self, agent_id="ather-agent"):
        self.agent_id = agent_id
        self.running = False
        self.cycles = 0
        self.created_at = datetime.utcnow()

    def start(self):
        self.running = True
        return "runtime_started"

    def stop(self):
        self.running = False
        return "runtime_stopped"

    def execute_cycle(self):
        if not self.running:
            raise RuntimeError("Runtime inactive")

        self.cycles += 1

        return {
            "cycle": self.cycles,
            "executed": True
        }

    def status(self):
        return {
            "agent": self.agent_id,
            "running": self.running,
            "cycles": self.cycles
        }
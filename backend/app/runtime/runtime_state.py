from enum import Enum


class RuntimeState(Enum):
    CREATED = "created"
    STARTING = "starting"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"


class RuntimeStateMachine:

    def __init__(self):
        self.state = RuntimeState.CREATED

    def transition(self, new_state):
        if not isinstance(new_state, RuntimeState):
            raise ValueError("Invalid state")

        self.state = new_state

        return self.state

    def current(self):
        return self.state.value
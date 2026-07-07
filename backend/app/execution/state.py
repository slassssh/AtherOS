class ExecutionState:


    def __init__(self):

        self.state = "created"


    def change(self, state):

        self.state = state

        return True


    def current(self):

        return self.state
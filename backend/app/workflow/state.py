class WorkflowState:


    def __init__(self):

        self.state = "created"


    def update(self, state):

        self.state = state

        return True


    def current(self):

        return self.state
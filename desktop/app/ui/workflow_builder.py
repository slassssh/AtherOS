class WorkflowBuilder:


    def __init__(self):

        self.steps = []



    def add_step(self, step):

        self.steps.append(
            step
        )

        return True



    def build(self):

        return {
            "workflow": self.steps
        }
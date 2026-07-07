class WorkflowCore:

    def __init__(self, name):

        self.name = name
        self.steps = []


    def add_step(self, step):

        self.steps.append(step)

        return True


    def info(self):

        return {
            "name": self.name,
            "steps": len(self.steps)
        }
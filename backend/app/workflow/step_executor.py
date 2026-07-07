class StepExecutor:

    def __init__(self):

        self.completed = []


    def execute(self, step):

        result = {
            "step": step,
            "success": True
        }

        self.completed.append(result)

        return result
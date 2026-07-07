class ExecutionNode:


    def __init__(self, name):

        self.name = name
        self.completed = False


    def execute(self):

        self.completed = True

        return {
            "node": self.name,
            "completed": True
        }
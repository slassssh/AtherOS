class MemoryWorkflowBinding:


    def __init__(self):

        self.memory = []


    def save(self, workflow_data):

        self.memory.append(
            workflow_data
        )

        return True


    def recall(self):

        return self.memory
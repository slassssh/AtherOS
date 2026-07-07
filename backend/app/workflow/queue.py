class WorkflowQueue:


    def __init__(self):

        self.queue = []


    def add(self, workflow):

        self.queue.append(workflow)

        return True


    def next(self):

        if self.queue:

            return self.queue.pop(0)

        return None
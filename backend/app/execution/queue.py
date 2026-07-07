class ExecutionQueue:


    def __init__(self):

        self.items = []


    def add(self, task):

        self.items.append(task)

        return True


    def next(self):

        if self.items:

            return self.items.pop(0)

        return None
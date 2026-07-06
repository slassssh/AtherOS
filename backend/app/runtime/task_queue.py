class TaskQueue:

    def __init__(self):

        self.tasks = []


    def add_task(self, task):

        self.tasks.append(task)

        return True


    def next_task(self):

        if self.tasks:

            return self.tasks.pop(0)

        return None


    def size(self):

        return len(self.tasks)
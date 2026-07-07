class TaskScheduler:


    def __init__(self):

        self.tasks = []



    def add(self, task):

        self.tasks.append(task)

        return True



    def all(self):

        return self.tasks
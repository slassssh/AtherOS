class TaskStore:


    def __init__(self):

        self.tasks = {}



    def save(self, task_id, task):

        self.tasks[task_id] = task

        return True



    def get(self, task_id):

        return self.tasks.get(
            task_id
        )
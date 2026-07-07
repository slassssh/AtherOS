class TaskBoard:


    def __init__(self):

        self.tasks = []



    def add_task(self, task):

        self.tasks.append(
            task
        )


        return True



    def show(self):

        return self.tasks
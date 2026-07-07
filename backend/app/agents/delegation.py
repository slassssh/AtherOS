class TaskDelegation:

    def __init__(self):

        self.tasks = {}


    def assign(self, agent, task):

        self.tasks[task] = agent

        return True


    def owner(self, task):

        return self.tasks.get(task)
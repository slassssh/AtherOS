from datetime import datetime


class ExecutionScheduler:


    def __init__(self):

        self.jobs = []


    def schedule(self, task):

        job = {
            "task": task,
            "time": datetime.utcnow()
        }

        self.jobs.append(job)

        return job
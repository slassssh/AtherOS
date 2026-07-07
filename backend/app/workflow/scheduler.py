from datetime import datetime


class WorkflowScheduler:


    def __init__(self):

        self.jobs = []


    def schedule(self, workflow):

        job = {
            "workflow": workflow,
            "time": datetime.utcnow()
        }

        self.jobs.append(job)

        return job


    def count(self):

        return len(self.jobs)
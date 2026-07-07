class BackgroundWorker:


    def __init__(self):

        self.jobs = []



    def add_job(self, job):

        self.jobs.append(
            job
        )

        return True



    def run_next(self):

        if self.jobs:

            return self.jobs.pop(0)


        return None
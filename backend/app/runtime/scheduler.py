from datetime import datetime


class TaskScheduler:

    def __init__(self):

        self.schedule = []


    def schedule_task(self, task):

        item = {
            "task": task,
            "time": datetime.utcnow()
        }

        self.schedule.append(item)

        return item


    def count(self):

        return len(self.schedule)
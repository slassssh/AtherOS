from datetime import datetime


class WorkflowLogs:


    def __init__(self):

        self.logs = []


    def add(self, message):

        entry = {
            "message": message,
            "time": datetime.utcnow()
        }

        self.logs.append(entry)

        return entry


    def history(self):

        return self.logs
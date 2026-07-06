from datetime import datetime


class RuntimeLogs:

    def __init__(self):

        self.logs = []


    def add(self, message):

        log = {
            "message": message,
            "time": datetime.utcnow()
        }

        self.logs.append(log)

        return log


    def history(self):

        return self.logs
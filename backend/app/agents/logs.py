from datetime import datetime


class MultiAgentLogs:

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
from datetime import datetime


class WorkflowEvents:


    def __init__(self):

        self.events = []


    def emit(self, event):

        data = {
            "event": event,
            "time": datetime.utcnow()
        }

        self.events.append(data)

        return data


    def all(self):

        return self.events
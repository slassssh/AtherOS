from datetime import datetime


class EventStream:

    def __init__(self):

        self.events = []


    def emit(self, event):

        data = {
            "event": event,
            "time": datetime.utcnow()
        }

        self.events.append(data)

        return data


    def stream(self):

        return self.events
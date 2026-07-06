from datetime import datetime


class ObserveModule:

    def __init__(self):
        self.observations = []


    def observe(self, data):

        event = {
            "data": data,
            "time": datetime.utcnow()
        }

        self.observations.append(event)

        return event


    def history(self):

        return self.observations
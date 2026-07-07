class TimelineViewer:


    def __init__(self):

        self.events = []



    def add_event(self, event):

        self.events.append(
            event
        )

        return True



    def timeline(self):

        return self.events
class HistoryTimeline:


    def __init__(self):

        self.events = []



    def add_event(self, event):

        self.events.append(
            event
        )


        return True



    def show(self):

        return self.events
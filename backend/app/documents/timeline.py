class DocumentTimeline:


    def __init__(self):

        self.events = []



    def add(self, event):

        self.events.append(
            event
        )


        return True



    def history(self):

        return self.events
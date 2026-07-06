"""
AtherOS Memory Timeline

Tracks memory events order.
"""


class MemoryTimeline:


    def __init__(self):

        self.events = []


    def add_event(
        self,
        event
    ):

        self.events.append(
            event
        )


    def history(self):

        return self.events.copy()
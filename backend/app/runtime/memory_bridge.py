class MemoryIntegration:

    def __init__(self):

        self.memory_events = []


    def store(self, data):

        self.memory_events.append(data)

        return True


    def recall(self):

        return self.memory_events
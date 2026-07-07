class MemoryDashboard:


    def __init__(self):

        self.memories = []



    def add_memory(self, memory):

        self.memories.append(
            memory
        )


        return True



    def show(self):

        return self.memories
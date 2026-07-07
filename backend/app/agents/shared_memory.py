class SharedMemory:

    def __init__(self):

        self.memory = []


    def add(self, data):

        self.memory.append(data)

        return True


    def recall(self):

        return self.memory
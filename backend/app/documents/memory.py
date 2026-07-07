class DocumentMemory:


    def __init__(self):

        self.memory = []



    def store(self, item):

        self.memory.append(item)

        return True



    def recall(self):

        return self.memory
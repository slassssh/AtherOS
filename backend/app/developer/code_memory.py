class CodeMemory:


    def __init__(self):

        self.memory = []



    def remember(self, data):

        self.memory.append(data)

        return True



    def recall(self):

        return self.memory
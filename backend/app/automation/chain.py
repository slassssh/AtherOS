class ChainAutomation:


    def __init__(self):

        self.chain = []



    def add(self, step):

        self.chain.append(step)

        return True



    def steps(self):

        return self.chain
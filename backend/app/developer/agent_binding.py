class AgentDeveloperBinding:


    def __init__(self):

        self.bindings = []



    def bind(self, agent):

        self.bindings.append(agent)

        return True



    def all(self):

        return self.bindings
class AgentWorkspaceBinding:


    def __init__(self):

        self.agents = []



    def bind(self, agent):

        self.agents.append(agent)

        return True



    def all(self):

        return self.agents
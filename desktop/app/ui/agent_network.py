class AgentNetworkView:


    def __init__(self):

        self.agents = []



    def register(self, agent):

        self.agents.append(
            agent
        )

        return True



    def view(self):

        return self.agents
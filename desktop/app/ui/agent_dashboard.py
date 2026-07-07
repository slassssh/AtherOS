class AgentDashboard:


    def __init__(self):

        self.agents = []



    def add_agent(self, agent):

        self.agents.append(
            agent
        )


        return True



    def display(self):

        return self.agents
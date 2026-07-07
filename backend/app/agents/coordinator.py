class MultiAgentCoordinator:

    def __init__(self):

        self.agents = []


    def add_agent(self, agent):

        self.agents.append(agent)

        return True


    def coordinate(self):

        return {
            "agents": len(self.agents),
            "coordinated": True
        }
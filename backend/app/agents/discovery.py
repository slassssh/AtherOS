class AgentDiscovery:

    def __init__(self):

        self.available_agents = []


    def announce(self, agent):

        self.available_agents.append(agent)

        return True


    def discover(self):

        return self.available_agents
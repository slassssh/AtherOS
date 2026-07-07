class AgentRegistry:

    def __init__(self):

        self.agents = {}


    def register(self, agent_id, agent):

        self.agents[agent_id] = agent

        return True


    def get(self, agent_id):

        return self.agents.get(agent_id)


    def all(self):

        return self.agents
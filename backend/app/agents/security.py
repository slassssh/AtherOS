class MultiAgentSecurity:

    def __init__(self):

        self.blocked = []


    def block_agent(self, agent):

        self.blocked.append(agent)

        return True


    def trusted(self, agent):

        return agent not in self.blocked
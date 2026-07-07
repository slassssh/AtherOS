class AgentProfile:


    def __init__(self, agent_id):

        self.agent_id = agent_id
        self.data = {}


    def update(self, key, value):

        self.data[key] = value

        return True


    def get(self, key):

        return self.data.get(key)
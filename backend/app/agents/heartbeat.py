from datetime import datetime


class AgentHeartbeat:

    def __init__(self):

        self.beats = {}


    def ping(self, agent):

        self.beats[agent] = datetime.utcnow()

        return True


    def status(self, agent):

        return agent in self.beats
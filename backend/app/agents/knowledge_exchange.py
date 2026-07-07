class KnowledgeExchange:

    def __init__(self):

        self.knowledge = []


    def share(self, agent, info):

        data = {
            "agent": agent,
            "info": info
        }

        self.knowledge.append(data)

        return data


    def all(self):

        return self.knowledge
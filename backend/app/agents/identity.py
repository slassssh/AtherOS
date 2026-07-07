import uuid


class AgentIdentity:


    def __init__(self, name):

        self.id = str(uuid.uuid4())
        self.name = name


    def info(self):

        return {
            "id": self.id,
            "name": self.name
        }
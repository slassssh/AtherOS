class AgentDocumentBinding:


    def __init__(self):

        self.bindings = []



    def bind(self, agent, document):

        self.bindings.append(
            {
                "agent": agent,
                "document": document
            }
        )


        return True



    def all(self):

        return self.bindings
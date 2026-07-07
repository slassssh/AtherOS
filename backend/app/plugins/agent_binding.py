class AgentPluginBinding:


    def __init__(self):

        self.bindings = []



    def bind(self, agent, plugin):

        self.bindings.append(
            {
                "agent": agent,
                "plugin": plugin
            }
        )

        return True



    def all(self):

        return self.bindings
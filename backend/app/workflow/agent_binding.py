class AgentWorkflowBinding:


    def __init__(self):

        self.bindings = {}


    def bind(self, workflow, agent):

        self.bindings[workflow] = agent

        return True


    def get_agent(self, workflow):

        return self.bindings.get(workflow)
class WorkflowSecurity:


    def __init__(self):

        self.blocked = []


    def block(self, workflow):

        self.blocked.append(workflow)

        return True


    def allowed(self, workflow):

        return workflow not in self.blocked
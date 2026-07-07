class WorkflowWorkspaceBinding:


    def __init__(self):

        self.workflows = []



    def bind(self, workflow):

        self.workflows.append(workflow)

        return True



    def all(self):

        return self.workflows
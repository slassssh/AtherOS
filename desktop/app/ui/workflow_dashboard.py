class WorkflowDashboard:


    def __init__(self):

        self.workflows = []



    def add_workflow(self, workflow):

        self.workflows.append(
            workflow
        )


        return True



    def list(self):

        return self.workflows
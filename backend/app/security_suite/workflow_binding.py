class WorkflowSecurityBinding:


    def bind(self, workflow):

        return {
            "workflow": workflow,
            "secured": True
        }
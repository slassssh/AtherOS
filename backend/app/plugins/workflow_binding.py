class WorkflowPluginBinding:


    def __init__(self):

        self.bindings = []



    def bind(self, workflow, plugin):

        self.bindings.append(
            {
                "workflow": workflow,
                "plugin": plugin
            }
        )

        return True



    def all(self):

        return self.bindings
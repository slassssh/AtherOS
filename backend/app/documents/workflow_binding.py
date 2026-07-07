class WorkflowDocumentBinding:


    def __init__(self):

        self.bindings = []



    def bind(self, workflow, document):

        self.bindings.append(
            {
                "workflow": workflow,
                "document": document
            }
        )


        return True



    def all(self):

        return self.bindings
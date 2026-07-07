class ToolWorkflowBinding:


    def __init__(self):

        self.tools = {}


    def attach(self, workflow, tool):

        self.tools[workflow] = tool

        return True


    def get_tool(self, workflow):

        return self.tools.get(workflow)
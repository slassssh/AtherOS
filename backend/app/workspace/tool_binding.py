class ToolWorkspaceBinding:


    def __init__(self):

        self.tools = []



    def bind(self, tool):

        self.tools.append(tool)

        return True



    def all(self):

        return self.tools
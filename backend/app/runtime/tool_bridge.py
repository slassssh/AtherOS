class ToolIntegration:

    def __init__(self):

        self.tools = {}


    def register(self, name, tool):

        self.tools[name] = tool

        return True


    def get_tool(self, name):

        return self.tools.get(name)


    def available(self):

        return list(self.tools.keys())
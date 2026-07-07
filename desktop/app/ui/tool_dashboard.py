class ToolDashboard:


    def __init__(self):

        self.tools = []



    def register(self, tool):

        self.tools.append(
            tool
        )


        return True



    def available(self):

        return self.tools
class SwarmExecution:

    def __init__(self):

        self.executions = []


    def execute(self, agents, task):

        result = {
            "agents": agents,
            "task": task,
            "success": True
        }

        self.executions.append(result)

        return result
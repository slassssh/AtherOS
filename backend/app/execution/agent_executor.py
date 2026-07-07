class AgentExecutor:


    def execute_agent(self, agent, task):

        return {
            "agent": agent,
            "task": task,
            "completed": True
        }
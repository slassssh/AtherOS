"""
AtherOS Execution Planner

Plans task execution order.
"""


class ExecutionPlanner:


    def plan(
        self,
        tasks
    ):


        return {
            "steps": tasks,
            "ready": True
        }
from backend.app.planner.plan import Plan
from backend.app.planner.task import Task


class Planner:

    def create_plan(self, goal: str) -> Plan:

        plan = Plan(goal=goal)

        plan.tasks.append(
            Task(
                description=goal
            )
        )

        return plan
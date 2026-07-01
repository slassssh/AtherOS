from backend.app.planner.plan import Plan
from backend.app.planner.task import Task


class Planner:

    def create_plan(self, goal: str) -> Plan:
        plan = Plan(goal=goal)

        tasks = self._decompose_goal(goal)

        # Create Task objects
        for description in tasks:
            plan.tasks.append(Task(description=description))

        # Add dependencies
        for i in range(1, len(plan.tasks)):
            plan.tasks[i].depends_on.append(
                plan.tasks[i - 1].task_id
            )

        return plan

    def _decompose_goal(self, goal: str) -> list[str]:
        goal_lower = goal.lower()

        tasks = []

        if "research" in goal_lower:
            tasks.append("Research topic")

        if "pdf" in goal_lower:
            tasks.append("Read PDF")

        if "summar" in goal_lower:
            tasks.append("Generate summary")

        if "powerpoint" in goal_lower or "presentation" in goal_lower:
            tasks.append("Create presentation")

        if "email" in goal_lower:
            tasks.append("Send email")

        if not tasks:
            tasks.append(goal)

        return tasks
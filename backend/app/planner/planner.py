from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from backend.app.planner.plan import Plan
from backend.app.planner.task import Task


class BasePlanner(ABC):
    """
    Abstract interface for planners in AtherOS.
    Allows swapping rule-based, heuristic, or LLM-backed planners.
    """

    @abstractmethod
    def create_plan(self, goal: str, context: Optional[Dict[str, Any]] = None) -> Plan:
        """
        Decompose a goal into a Plan containing tasks and dependency graphs.
        """
        pass


class Planner(BasePlanner):
    """
    Standard heuristic/rule-based planner.
    Can be replaced by an LLM-backed planner in later stages.
    """

    def create_plan(self, goal: str, context: Optional[Dict[str, Any]] = None) -> Plan:
        plan = Plan(goal=goal)

        decomposed = self._decompose_goal(goal)

        for item in decomposed:
            if isinstance(item, dict):
                task = Task(
                    description=item.get("description", goal),
                    tool=item.get("tool"),
                    tool_input=item.get("tool_input", {})
                )
            else:
                task = Task(description=str(item))
            plan.tasks.append(task)

        # Build sequential dependency chain as baseline
        for i in range(1, len(plan.tasks)):
            plan.tasks[i].depends_on.append(
                plan.tasks[i - 1].task_id
            )

        return plan

    def _decompose_goal(self, goal: str) -> List[Any]:
        goal_lower = goal.lower()
        tasks = []

        if "file" in goal_lower or "read" in goal_lower or "write" in goal_lower or "log" in goal_lower:
            tasks.append({
                "description": f"Perform file operation for: {goal}",
                "tool": "file",
                "tool_input": {"action": "list", "path": "."}
            })

        if "code" in goal_lower or "python" in goal_lower or "calculate" in goal_lower:
            tasks.append({
                "description": f"Execute Python task: {goal}",
                "tool": "python",
                "tool_input": {"code": "print('Executing task execution pipeline')"}
            })

        if "terminal" in goal_lower or "command" in goal_lower or "system" in goal_lower:
            tasks.append({
                "description": f"Execute terminal command: {goal}",
                "tool": "terminal",
                "tool_input": {"command": "echo AtherOS Execution Engine"}
            })

        if not tasks:
            tasks.append({
                "description": goal,
                "tool": None,
                "tool_input": {}
            })

        return tasks
from typing import Any, Dict, Optional
from backend.app.llm.base import BaseLLMProvider
from backend.app.llm.factory import LLMFactory
from backend.app.planner.plan import Plan
from backend.app.planner.planner import BasePlanner, Planner
from backend.app.planner.task import Task
from backend.app.utils.logger import logger


class LLMPlanner(BasePlanner):
    """
    LLM-backed Intelligent Goal Decomposition Planner.
    Implements BasePlanner and depends solely on BaseLLMProvider interface.
    """

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm_provider = llm_provider or LLMFactory.create_provider()
        self.fallback_planner = Planner()

    def create_plan(self, goal: str, context: Optional[Dict[str, Any]] = None) -> Plan:
        schema = {
            "type": "object",
            "properties": {
                "goal": {"type": "string"},
                "tasks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": {"type": "string"},
                            "tool": {"type": "string", "enum": ["file", "python", "terminal", None]},
                            "tool_input": {"type": "object"}
                        },
                        "required": ["description"]
                    }
                }
            },
            "required": ["goal", "tasks"]
        }

        system_prompt = (
            "You are the Lead Planning Agent for AtherOS AI Operating System. "
            "Decompose user goals into a sequential list of precise tasks, selecting available tools "
            "('file', 'python', 'terminal', or null)."
        )

        try:
            structured_plan = self.llm_provider.generate_structured(
                prompt=goal,
                schema=schema,
                system_prompt=system_prompt
            )

            plan = Plan(goal=goal)
            tasks_data = structured_plan.get("tasks", [])

            for task_info in tasks_data:
                task = Task(
                    description=task_info.get("description", goal),
                    tool=task_info.get("tool"),
                    tool_input=task_info.get("tool_input", {})
                )
                plan.tasks.append(task)

            # Build sequential dependency chain
            for i in range(1, len(plan.tasks)):
                plan.tasks[i].depends_on.append(plan.tasks[i - 1].task_id)

            if plan.tasks:
                return plan

        except Exception as err:
            logger.warning(f"LLMPlanner decomposition failed: {err}. Falling back to standard heuristic planner.")

        return self.fallback_planner.create_plan(goal, context)

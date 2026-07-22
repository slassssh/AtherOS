import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest
from backend.app.core.engine import Engine
from backend.app.core.journal import Journal
from backend.app.planner.planner import BasePlanner, Planner
from backend.app.planner.task import Task, TaskStatus
from backend.app.planner.plan import Plan
from backend.app.core.tool_executor import BaseToolExecutor, ToolExecutor
from backend.app.tools.result import ToolResult


class MockCustomPlanner(BasePlanner):
    def create_plan(self, goal: str, context=None) -> Plan:
        plan = Plan(goal=goal)
        task1 = Task(description="Step 1: Read files", tool="file", tool_input={"action": "list", "path": "."})
        task2 = Task(description="Step 2: Process data", tool="python", tool_input={"code": "res = 21 * 2"})
        task2.depends_on.append(task1.task_id)
        plan.tasks.extend([task1, task2])
        return plan


class MockCustomToolExecutor(BaseToolExecutor):
    def execute(self, tool_name: str, **kwargs) -> ToolResult:
        if tool_name == "file":
            return ToolResult(success=True, output=["file1.txt", "file2.txt"])
        if tool_name == "python":
            return ToolResult(success=True, output="42")
        return ToolResult(success=False, error="Unknown tool")


def test_engine_dependency_injection():
    journal = Journal()
    planner = MockCustomPlanner()
    executor = MockCustomToolExecutor()

    engine = Engine(journal=journal, planner=planner, tool_executor=executor)

    assert engine.planner == planner
    assert engine.tool_executor == executor
    assert engine.journal == journal


def test_engine_execute_goal_pipeline():
    engine = Engine(planner=MockCustomPlanner(), tool_executor=MockCustomToolExecutor())
    result = engine.execute_goal("Test execution pipeline goal")

    assert result["status"] == "COMPLETED"
    assert len(result["tasks"]) == 2
    assert result["tasks"][0]["status"] == "COMPLETED"
    assert result["tasks"][0]["tool_name"] == "file"
    assert result["tasks"][0]["output"] == ["file1.txt", "file2.txt"]
    assert result["tasks"][1]["status"] == "COMPLETED"
    assert result["tasks"][1]["output"] == "42"

    # Journal verification
    events = engine.journal.get_events()
    event_types = [e.event_type.value for e in events]
    assert "SESSION_CREATED" in event_types
    assert "PLAN_CREATED" in event_types
    assert "TASK_STARTED" in event_types
    assert "TASK_COMPLETED" in event_types
    assert "SESSION_COMPLETED" in event_types


def test_structured_task_result():
    task = Task(description="Sample Task", tool="terminal", tool_input={"command": "dir"})
    task.status = TaskStatus.COMPLETED
    task.output = "Directory listing output"
    task.execution_time = 0.052

    res_dict = task.to_dict()
    assert res_dict["description"] == "Sample Task"
    assert res_dict["tool_name"] == "terminal"
    assert res_dict["status"] == "COMPLETED"
    assert res_dict["output"] == "Directory listing output"
    assert res_dict["execution_time"] == 0.052

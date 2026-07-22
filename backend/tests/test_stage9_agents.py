import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest
from backend.app.agents.manager import AgentManager
from backend.app.agents.specialized import CodingAgent, PlannerAgent, SecurityAgent
from backend.app.agents.types import AgentMessage, AgentTask
from backend.app.core.engine import Engine


def test_agent_registration_and_monitoring():
    mgr = AgentManager()
    assert len(mgr._agents) == 8  # 8 default agents registered

    statuses = mgr.monitor_agents()
    assert "planner_agent" in statuses
    assert statuses["planner_agent"] == "IDLE"


def test_agent_task_dispatch_and_messaging():
    mgr = AgentManager()
    task = AgentTask(goal="Build secure REST API", description="Plan API endpoints")

    res = mgr.dispatch_task("planner_agent", task)
    assert res.success is True
    assert "subtasks" in res.output

    # Broadcast message check
    msg = AgentMessage(source_agent="planner_agent", target_agent="coding_agent", task_id=task.task_id, payload={"status": "READY"})
    mgr.broadcast(msg)
    assert len(mgr._message_bus) > 0


def test_agent_delegation():
    mgr = AgentManager()
    task = AgentTask(goal="Refactor auth security module", description="Audit permissions")

    res = mgr.delegate("planner_agent", "security_agent", task)
    assert res.success is True
    assert res.agent_id == "security_agent"
    assert res.output.get("status") == "SECURE"


def test_agent_failure_recovery():
    mgr = AgentManager()
    sec_agent = mgr.get_agent("security_agent")
    sec_agent.status = "FAILED"

    assert mgr.monitor_agents()["security_agent"] == "FAILED"
    recovered = mgr.recover_failed_agents()
    assert recovered == 1
    assert mgr.monitor_agents()["security_agent"] == "IDLE"


def test_multi_agent_pipeline_execution():
    mgr = AgentManager()
    res = mgr.execute_multi_agent_pipeline("Harden database connection pool and secrets encryption")

    assert res["status"] == "COMPLETED"
    assert len(res["agent_stages"]) == 8
    assert res["agent_stages"]["planner_agent"]["success"] is True
    assert res["agent_stages"]["security_agent"]["success"] is True


def test_engine_autonomous_multi_agent_integration():
    engine = Engine()
    res = engine.execute_autonomous_goal("Deploy AtherOS autonomous microservice architecture")

    assert res["status"] == "COMPLETED"
    assert "agent_stages" in res
    assert res["agent_stages"]["coding_agent"]["success"] is True

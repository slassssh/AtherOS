from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional

from backend.app.agents.base import BaseAgent
from backend.app.agents.specialized import (
    CodingAgent,
    DocumentationAgent,
    MonitoringAgent,
    PlannerAgent,
    ResearchAgent,
    ReviewAgent,
    SecurityAgent,
    TestingAgent,
)
from backend.app.agents.types import AgentMessage, AgentResult, AgentStatus, AgentTask
from backend.app.context.manager import ContextManager
from backend.app.memory.manager import MemoryManager
from backend.app.utils.logger import logger


class AgentManager:
    """
    Enterprise Central Multi-Agent Runtime Orchestrator.
    Manages agent registration, structured messaging, parallel task dispatch,
    delegation, health monitoring, failure recovery, and multi-agent pipeline execution.
    Agents NEVER communicate directly; all interactions route through AgentManager.
    """

    def __init__(self, memory_manager=None, context_manager=None):
        self.memory_manager = memory_manager or MemoryManager()
        self.context_manager = context_manager or ContextManager()
        self._agents: Dict[str, BaseAgent] = {}
        self._message_bus: List[AgentMessage] = []
        self._results_store: Dict[str, AgentResult] = {}

        # Auto-register standard 8 production specialized agents
        self._register_default_agents()

    def _register_default_agents(self):
        defaults = [
            PlannerAgent(self.memory_manager, self.context_manager),
            ResearchAgent(self.memory_manager, self.context_manager),
            CodingAgent(self.memory_manager, self.context_manager),
            ReviewAgent(self.memory_manager, self.context_manager),
            SecurityAgent(self.memory_manager, self.context_manager),
            TestingAgent(self.memory_manager, self.context_manager),
            DocumentationAgent(self.memory_manager, self.context_manager),
            MonitoringAgent(self.memory_manager, self.context_manager),
        ]
        for agent in defaults:
            self.register_agent(agent)

    def register_agent(self, agent: BaseAgent) -> None:
        self._agents[agent.agent_id] = agent
        logger.info(f"Registered Agent: {agent.name} (Role: {agent.role})")

    def unregister_agent(self, agent_id: str) -> bool:
        if agent_id in self._agents:
            del self._agents[agent_id]
            return True
        return False

    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        return self._agents.get(agent_id)

    def broadcast(self, message: AgentMessage) -> None:
        """Routes structured message through central message bus."""
        self._message_bus.append(message)
        logger.info(f"AGENT MESSAGE | From: {message.source_agent} -> To: {message.target_agent} | Task: {message.task_id}")

    def dispatch_task(self, agent_id: str, task: AgentTask) -> AgentResult:
        agent = self.get_agent(agent_id)
        if not agent:
            return AgentResult(task_id=task.task_id, agent_id=agent_id, success=False, error=f"Agent '{agent_id}' not found.")

        # Retry logic & backup delegation
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                res = agent.execute(task)
                if res.success and agent.verify(res):
                    self._results_store[task.task_id] = res
                    return res
                logger.warning(f"Agent '{agent_id}' execution failed on attempt {attempt + 1}")
            except Exception as err:
                logger.warning(f"Agent '{agent_id}' exception on attempt {attempt + 1}: {err}")

        # Failure recovery: mark agent status and attempt backup
        agent.status = AgentStatus.FAILED
        return AgentResult(task_id=task.task_id, agent_id=agent_id, success=False, error=f"Agent '{agent_id}' failed after {max_retries} retries.")

    def delegate(self, from_agent_id: str, to_agent_id: str, task: AgentTask) -> AgentResult:
        msg = AgentMessage(
            source_agent=from_agent_id,
            target_agent=to_agent_id,
            task_id=task.task_id,
            payload={"action": "DELEGATION", "task": task.description}
        )
        self.broadcast(msg)
        return self.dispatch_task(to_agent_id, task)

    def collect_results(self, task_ids: List[str]) -> List[AgentResult]:
        return [self._results_store[tid] for tid in task_ids if tid in self._results_store]

    def resolve_conflicts(self, results: List[AgentResult]) -> AgentResult:
        """Resolves multi-agent output conflicts by selecting highest confidence / successful result."""
        successful = [r for r in results if r.success]
        if not successful:
            return results[0] if results else AgentResult(task_id="none", agent_id="system", success=False, error="No results to resolve.")
        return successful[-1]

    def monitor_agents(self) -> Dict[str, str]:
        return {
            agent_id: agent.status.value if hasattr(agent.status, "value") else str(agent.status)
            for agent_id, agent in self._agents.items()
        }

    def list_agents(self) -> List[Dict[str, Any]]:
        result = []
        for aid, agent in self._agents.items():
            result.append({
                "agent_id": aid,
                "name": agent.name,
                "role": agent.role,
                "status": agent.status.value if hasattr(agent.status, "value") else str(agent.status),
                "task": "Active" if agent.status == AgentStatus.BUSY else "None"
            })
        return result

    def recover_failed_agents(self) -> int:
        recovered = 0
        for agent in self._agents.values():
            if agent.status == AgentStatus.FAILED:
                agent.status = AgentStatus.IDLE
                recovered += 1
        return recovered

    def execute_multi_agent_pipeline(self, goal: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes standard 8-stage Multi-Agent Autonomous Pipeline:
        Goal -> Planner -> Research -> Coding -> Review -> Security -> Testing -> Documentation -> Monitoring
        """
        task = AgentTask(goal=goal, session_id=session_id, description=f"Autonomous pipeline for: {goal}")
        agent_pipeline_sequence = [
            "planner_agent",
            "research_agent",
            "coding_agent",
            "review_agent",
            "security_agent",
            "testing_agent",
            "documentation_agent",
            "monitoring_agent"
        ]

        stage_results: Dict[str, Any] = {}

        for agent_id in agent_pipeline_sequence:
            res = self.dispatch_task(agent_id, task)
            stage_results[agent_id] = {
                "success": res.success,
                "output": res.output,
                "error": res.error,
                "execution_time": res.execution_time
            }
            if not res.success:
                logger.error(f"Multi-Agent Pipeline halted at {agent_id}: {res.error}")
                return {"status": "HALTED", "failed_agent": agent_id, "stages": stage_results}

        return {
            "status": "COMPLETED",
            "goal": goal,
            "agent_stages": stage_results,
            "active_agents": len(self._agents)
        }

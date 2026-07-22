from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from backend.app.agents.types import AgentResult, AgentStatus, AgentTask
from backend.app.context.manager import ContextManager
from backend.app.memory.manager import MemoryManager


class BaseAgent(ABC):
    """
    Abstract Base Class for all AtherOS Autonomous Agents.
    Every agent must implement plan, execute, verify, report, and learn.
    """

    def __init__(
        self,
        agent_id: str,
        name: str,
        role: str,
        memory_manager: Optional[MemoryManager] = None,
        context_manager: Optional[ContextManager] = None
    ):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.status = AgentStatus.IDLE
        self.memory_manager = memory_manager or MemoryManager()
        self.context_manager = context_manager or ContextManager()

    @abstractmethod
    def plan(self, task: AgentTask) -> Dict[str, Any]:
        """Formulates an execution plan for the agent task."""
        pass

    @abstractmethod
    def execute(self, task: AgentTask) -> AgentResult:
        """Executes the specific agent task."""
        pass

    @abstractmethod
    def verify(self, result: AgentResult) -> bool:
        """Verifies the correctness and safety of the execution result."""
        pass

    @abstractmethod
    def report(self, result: AgentResult) -> Dict[str, Any]:
        """Generates a structured report summary of the agent execution."""
        pass

    @abstractmethod
    def learn(self, result: AgentResult) -> None:
        """Stores lessons learned into MemoryManager and Knowledge Graph."""
        pass

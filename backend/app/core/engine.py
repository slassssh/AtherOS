import time
from typing import Any, Dict, List, Optional

from backend.app.agents.manager import AgentManager
from backend.app.cluster.manager import ClusterManager
from backend.app.context.manager import ContextManager
from backend.app.context.types import NodeType, RelationType
from backend.app.core.events import (
    ActorType,
    EventType,
    JournalEvent,
    SessionState,
)
from backend.app.core.journal import Journal
from backend.app.core.session import Session
from backend.app.core.state_machine import StateMachine
from backend.app.core.tool_executor import BaseToolExecutor, ToolExecutor
from backend.app.events.bus import EventBus
from backend.app.events.types import SystemEvent, SystemEventType
from backend.app.llm.orchestrator import ModelManager
from backend.app.memory.manager import MemoryManager
from backend.app.memory.memory_item import MemoryItem
from backend.app.planner.plan import Plan
from backend.app.planner.planner import BasePlanner, Planner
from backend.app.planner.task import Task, TaskStatus
from backend.app.plugins.base import PluginContext
from backend.app.plugins.manager import PluginManager
from backend.app.registry.capabilities import CapabilityRegistry


class Engine:
    """
    Core orchestration engine.
    Coordinates sessions, planning, tool execution, journal events, enterprise memory,
    Knowledge Graph context, Autonomous Multi-Agent Runtime, System Event Bus, Plugin Manager, AI Model Orchestrator, and Cluster Manager.
    Communicates ONLY via public interfaces and APIs.
    Depends on abstract interfaces (BasePlanner, BaseToolExecutor) via dependency injection.
    """

    def __init__(
        self,
        journal: Optional[Journal] = None,
        planner: Optional[BasePlanner] = None,
        tool_executor: Optional[BaseToolExecutor] = None,
        memory_manager: Optional[MemoryManager] = None,
        context_manager: Optional[ContextManager] = None,
        agent_manager: Optional[AgentManager] = None,
        event_bus: Optional[EventBus] = None,
        capability_registry: Optional[CapabilityRegistry] = None,
        plugin_manager: Optional[PluginManager] = None,
        model_manager: Optional[ModelManager] = None,
        cluster_manager: Optional[ClusterManager] = None,
    ) -> None:
        self.journal = journal or Journal()
        self.planner = planner or Planner()
        self.tool_executor = tool_executor or ToolExecutor()
        self.memory_manager = memory_manager or MemoryManager()
        self.context_manager = context_manager or ContextManager()
        self.agent_manager = agent_manager or AgentManager(self.memory_manager, self.context_manager)
        self.event_bus = event_bus or EventBus()
        self.capability_registry = capability_registry or CapabilityRegistry()
        self.model_manager = model_manager or ModelManager()
        self.cluster_manager = cluster_manager or ClusterManager(self.memory_manager, self.event_bus)

        # Initialize Plugin Context Gateway and Plugin Manager
        self.plugin_context = PluginContext(
            memory_manager=self.memory_manager,
            context_manager=self.context_manager,
            agent_manager=self.agent_manager,
            capability_registry=self.capability_registry,
            event_bus=self.event_bus,
            journal=self.journal
        )
        self.plugin_manager = plugin_manager or PluginManager(self.plugin_context)

        # Register core capabilities
        self._register_subsystem_capabilities()

    def _register_subsystem_capabilities(self):
        self.capability_registry.register("Engine", self)
        self.capability_registry.register("Planner", self.planner)
        self.capability_registry.register("ToolExecutor", self.tool_executor)
        self.capability_registry.register("MemoryManager", self.memory_manager)
        self.capability_registry.register("ContextManager", self.context_manager)
        self.capability_registry.register("AgentManager", self.agent_manager)
        self.capability_registry.register("PluginManager", self.plugin_manager)
        self.capability_registry.register("ModelManager", self.model_manager)
        self.capability_registry.register("ClusterManager", self.cluster_manager)

    def create_session(
        self,
        title: str,
        description: str,
    ) -> Session:

        session = Session(
            title=title,
            description=description,
        )

        event = JournalEvent(
            session_id=session.session_id,
            sequence_number=1,
            event_type=EventType.SESSION_CREATED,
            actor=ActorType.SYSTEM,
            payload={
                "title": title,
                "description": description,
            },
        )

        self.journal.add_event(event)

        # 1. Store Session Memory via MemoryManager
        self.memory_manager.store(MemoryItem(
            content=f"Session Created: {title} - {description}",
            layer="session",
            source="ENGINE",
            session_id=str(session.session_id),
            importance=5,
            tags=["session_init"]
        ))

        # 2. Register Session Node in Knowledge Graph via ContextManager
        self.context_manager.create_node(
            node_type=NodeType.SESSION,
            label=title,
            properties={"description": description, "state": session.state.value},
            node_id=str(session.session_id)
        )

        # 3. Publish System Event to EventBus
        self.event_bus.publish(SystemEvent(
            source="Engine",
            type=SystemEventType.GOAL_CREATED,
            payload={"session_id": str(session.session_id), "title": title},
            correlation_id=str(session.session_id)
        ))

        return session

    def transition(
        self,
        session: Session,
        new_state: SessionState,
    ) -> bool:

        if not StateMachine.can_transition(
            session.state,
            new_state,
        ):
            return False

        session.state = new_state

        event = JournalEvent(
            session_id=session.session_id,
            sequence_number=self.journal.event_count() + 1,
            event_type=EventType.STATE_CHANGED,
            actor=ActorType.ENGINE,
            payload={
                "new_state": new_state.value,
            },
        )

        self.journal.add_event(event)

        # Update Working Memory state & Context Node properties
        self.memory_manager.store(MemoryItem(
            content=f"Engine state transition to {new_state.value}",
            layer="working",
            source="ENGINE",
            session_id=str(session.session_id),
            importance=3,
            tags=["state_transition"]
        ))

        self.context_manager.update_node(
            node_id=str(session.session_id),
            properties={"state": new_state.value}
        )

        return True

    def get_ready_tasks(self, plan: Plan) -> List[Task]:
        ready = []

        task_lookup = {
            task.task_id: task
            for task in plan.tasks
        }

        for task in plan.tasks:
            if task.status != TaskStatus.PENDING:
                continue

            can_run = True

            for dependency in task.depends_on:
                dep_task = task_lookup.get(dependency)
                if dep_task and dep_task.status != TaskStatus.COMPLETED:
                    can_run = False
                    break

            if can_run:
                ready.append(task)

        return ready

    def execute_task(self, task: Task, session_id: Any = None) -> Dict[str, Any]:
        """
        Executes a single task strictly via the ToolExecutor gateway and updates Knowledge Graph.
        """
        start_time = time.time()
        task.status = TaskStatus.RUNNING

        # 1. Log Task Started Event & Create Task Node in Graph
        self.journal.add_event(JournalEvent(
            session_id=session_id,
            sequence_number=self.journal.event_count() + 1,
            event_type=EventType.TASK_STARTED,
            actor=ActorType.ENGINE,
            payload={
                "task_id": str(task.task_id),
                "description": task.description,
                "tool": task.tool,
            }
        ))

        task_node = self.context_manager.create_node(
            node_type=NodeType.TASK,
            label=task.description,
            properties={"status": task.status.value, "tool": task.tool},
            node_id=str(task.task_id)
        )

        if session_id:
            self.context_manager.create_edge(
                source_id=str(session_id),
                target_id=str(task.task_id),
                relation_type=RelationType.CREATED
            )

        try:
            # 2. Invoke tool strictly through ToolExecutor gateway (if tool specified)
            if task.tool:
                # Link Tool Node in Knowledge Graph
                tool_node = self.context_manager.create_node(
                    node_type=NodeType.TOOL,
                    label=task.tool,
                    properties={"tool_name": task.tool}
                )
                self.context_manager.create_edge(
                    source_id=str(task.task_id),
                    target_id=tool_node.node_id,
                    relation_type=RelationType.USES
                )

                tool_result = self.tool_executor.execute(task.tool, **task.tool_input)

                self.journal.add_event(JournalEvent(
                    session_id=session_id,
                    sequence_number=self.journal.event_count() + 1,
                    event_type=EventType.RESPONSE_GENERATED,
                    actor=ActorType.TOOL,
                    payload={
                        "task_id": str(task.task_id),
                        "tool": task.tool,
                        "success": tool_result.success,
                        "output": tool_result.output,
                        "error": tool_result.error,
                    }
                ))

                # Store Tool Output in Tool Memory layer
                self.memory_manager.store(MemoryItem(
                    content=str(tool_result.output or tool_result.error or ""),
                    layer="tool",
                    source="TOOL",
                    session_id=str(session_id) if session_id else None,
                    importance=6,
                    tags=["tool_output", task.tool],
                    metadata={"tool": task.tool, "success": tool_result.success}
                ))

                if tool_result.success:
                    task.output = tool_result.output
                    task.status = TaskStatus.COMPLETED
                    self.context_manager.create_edge(
                        source_id=str(task.task_id),
                        target_id=tool_node.node_id,
                        relation_type=RelationType.SUCCEEDED
                    )
                else:
                    task.error = tool_result.error or "Tool execution failed"
                    task.retry_count += 1
                    if task.retry_count >= task.max_retries:
                        task.status = TaskStatus.FAILED
                    else:
                        task.status = TaskStatus.PENDING
                    self.context_manager.create_edge(
                        source_id=str(task.task_id),
                        target_id=tool_node.node_id,
                        relation_type=RelationType.FAILED
                    )
            else:
                task.output = f"Task '{task.description}' completed without tool execution."
                task.status = TaskStatus.COMPLETED

            task.execution_time = time.time() - start_time

            # Update Task Node Status in Graph
            self.context_manager.update_node(
                node_id=str(task.task_id),
                properties={"status": task.status.value, "execution_time": task.execution_time}
            )

            # 3. Log Task Completed / Failed Event & Store Episodic Memory
            event_type = EventType.TASK_COMPLETED if task.status == TaskStatus.COMPLETED else EventType.TASK_FAILED
            self.journal.add_event(JournalEvent(
                session_id=session_id,
                sequence_number=self.journal.event_count() + 1,
                event_type=event_type,
                actor=ActorType.ENGINE,
                payload=task.to_dict()
            ))

            self.memory_manager.store(MemoryItem(
                content=f"Task {task.description} -> Status: {task.status.value}",
                layer="episodic",
                source="ENGINE",
                session_id=str(session_id) if session_id else None,
                importance=7,
                tags=["task_result"]
            ))

            return task.to_dict()

        except Exception as error:
            task.execution_time = time.time() - start_time
            task.error = str(error)
            task.retry_count += 1
            task.status = TaskStatus.FAILED

            self.journal.add_event(JournalEvent(
                session_id=session_id,
                sequence_number=self.journal.event_count() + 1,
                event_type=EventType.TASK_FAILED,
                actor=ActorType.ENGINE,
                payload=task.to_dict()
            ))

            return task.to_dict()

    def execute_goal(self, goal: str, session: Optional[Session] = None) -> Dict[str, Any]:
        """
        Executes a user goal end-to-end through the pipeline.
        Populates Knowledge Graph with Goal -> Plan -> Task -> Tool relationships.
        """
        if session is None:
            session = self.create_session("AtherOS Goal Session", goal)

        # 1. Create Goal Node in Knowledge Graph & Link to Session Node
        goal_node = self.context_manager.create_node(
            node_type=NodeType.GOAL,
            label=goal,
            properties={"goal_text": goal}
        )
        self.context_manager.create_edge(
            source_id=str(session.session_id),
            target_id=goal_node.node_id,
            relation_type=RelationType.CREATED
        )

        # 2. Store Goal in Session & Long-Term Memory
        self.memory_manager.store(MemoryItem(
            content=f"User Goal: {goal}",
            layer="session",
            source="USER",
            session_id=str(session.session_id),
            importance=9,
            tags=["goal"]
        ))

        # 3. Planning Started
        self.transition(session, SessionState.PLANNING)
        self.journal.add_event(JournalEvent(
            session_id=session.session_id,
            sequence_number=self.journal.event_count() + 1,
            event_type=EventType.PLAN_CREATED,
            actor=ActorType.PLANNER,
            payload={"status": "PLANNING_STARTED", "goal": goal}
        ))

        # 4. Planning Execution & Plan Node Graph Link
        plan = self.planner.create_plan(goal)
        plan_node = self.context_manager.create_node(
            node_type=NodeType.PLAN,
            label=f"Plan for: {goal[:30]}",
            properties={"task_count": len(plan.tasks)}
        )
        self.context_manager.create_edge(
            source_id=goal_node.node_id,
            target_id=plan_node.node_id,
            relation_type=RelationType.GENERATED
        )

        # 5. Planning Completed Event
        self.journal.add_event(JournalEvent(
            session_id=session.session_id,
            sequence_number=self.journal.event_count() + 1,
            event_type=EventType.PLAN_CREATED,
            actor=ActorType.PLANNER,
            payload={
                "status": "PLANNING_COMPLETED",
                "goal": goal,
                "task_count": len(plan.tasks),
                "tasks": [t.description for t in plan.tasks]
            }
        ))

        self.transition(session, SessionState.EXECUTING)

        # 6. Pipeline Task Execution Loop & Task Dependency Edges
        task_results = []
        for t in plan.tasks:
            t_node = self.context_manager.create_node(
                node_type=NodeType.TASK,
                label=t.description,
                node_id=str(t.task_id)
            )
            self.context_manager.create_edge(
                source_id=plan_node.node_id,
                target_id=t_node.node_id,
                relation_type=RelationType.CHILD_OF
            )
            for dep_id in t.depends_on:
                self.context_manager.create_edge(
                    source_id=str(dep_id),
                    target_id=str(t.task_id),
                    relation_type=RelationType.DEPENDS_ON
                )

        while True:
            ready_tasks = self.get_ready_tasks(plan)
            if not ready_tasks:
                break

            for task in ready_tasks:
                res = self.execute_task(task, session_id=session.session_id)
                task_results.append(res)
                if task.status == TaskStatus.FAILED:
                    break

            if any(t.status == TaskStatus.FAILED for t in plan.tasks):
                break

        # 7. Determine Final Session State & Journal Event
        all_completed = all(t.status == TaskStatus.COMPLETED for t in plan.tasks)
        if all_completed and plan.tasks:
            self.transition(session, SessionState.GENERATING_RESPONSE)
            self.transition(session, SessionState.COMPLETED)
            self.journal.add_event(JournalEvent(
                session_id=session.session_id,
                sequence_number=self.journal.event_count() + 1,
                event_type=EventType.SESSION_COMPLETED,
                actor=ActorType.ENGINE,
                payload={"goal": goal, "status": "GOAL_COMPLETED"}
            ))

            # Store Goal Completion in Long-Term Memory
            self.memory_manager.store(MemoryItem(
                content=f"Goal Successfully Executed: {goal}",
                layer="long_term",
                source="ENGINE",
                session_id=str(session.session_id),
                importance=8,
                tags=["goal_completed"]
            ))
        else:
            self.transition(session, SessionState.FAILED)
            self.journal.add_event(JournalEvent(
                session_id=session.session_id,
                sequence_number=self.journal.event_count() + 1,
                event_type=EventType.ERROR_OCCURRED,
                actor=ActorType.ENGINE,
                payload={"goal": goal, "status": "GOAL_FAILED"}
            ))

        return {
            "session_id": str(session.session_id),
            "goal": goal,
            "status": session.state.value,
            "tasks": [t.to_dict() for t in plan.tasks],
            "event_count": self.journal.event_count(),
        }

    def execute_autonomous_goal(self, goal: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes a goal using the Autonomous Multi-Agent Runtime orchestrator.
        """
        return self.agent_manager.execute_multi_agent_pipeline(goal, session_id=session_id)
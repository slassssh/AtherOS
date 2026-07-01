"""
AtherOS Core Engine

Coordinates sessions, journal events,
and state transitions.
"""

from backend.app.core.events import (
    ActorType,
    EventType,
    JournalEvent,
    SessionState,
)

from backend.app.core.journal import Journal
from backend.app.core.session import Session
from backend.app.core.state_machine import StateMachine
from backend.app.planner.plan import Plan
from backend.app.planner.task import TaskStatus


class Engine:
    """
    Core orchestration engine.
    """

    def __init__(self) -> None:
        self.journal = Journal()

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
            },
        )

        self.journal.add_event(event)

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

        return True

  

    def get_ready_tasks(self, plan: Plan):
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
                if task_lookup[dependency].status != TaskStatus.COMPLETED:
                    can_run = False
                    break

            if can_run:
                ready.append(task)

        return ready

    def execute_task(self, task):
        """
        Simulate execution of a task.
        Later this will call the Tool Registry.
        """

        from backend.app.planner.task import TaskStatus

        task.status = TaskStatus.RUNNING

        # Tool execution will happen here later

        task.status = TaskStatus.COMPLETED

        event = JournalEvent(
            session_id=None,   # We'll replace this with the real session later
            sequence_number=self.journal.event_count() + 1,
            event_type=EventType.TASK_COMPLETED,
            actor=ActorType.ENGINE,
            payload={
                "task": task.description,
            },
        )

        self.journal.add_event(event)
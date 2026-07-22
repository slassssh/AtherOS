import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest
from backend.app.database.connection import DatabaseConnection
from backend.app.database.models import MemoryModel, SessionModel, JournalEventModel
from backend.app.database.repository import (
    UnitOfWork,
    SessionRepository,
    MemoryRepository,
    JournalRepository,
)
from backend.app.memory.long_term import LongTermMemory
from backend.app.memory.model import Memory
from backend.app.core.journal import Journal
from backend.app.core.events import JournalEvent, EventType, ActorType


@pytest.fixture(autouse=True)
def setup_db():
    db = DatabaseConnection()
    db.connect()
    yield db


def test_unit_of_work_commit_and_crud():
    with UnitOfWork() as uow:
        repo = SessionRepository(uow.session)
        session_entity = SessionModel(title="Test DB Session", description="Database testing", state="INIT")
        saved = repo.save(session_entity)
        session_id = saved.id

    # Verify persistence after commit
    with UnitOfWork() as uow:
        repo = SessionRepository(uow.session)
        fetched = repo.get(session_id)
        assert fetched is not None
        assert fetched.title == "Test DB Session"
        assert fetched.state == "INIT"
        assert fetched.is_deleted is False


def test_unit_of_work_rollback_on_failure():
    failed_id = None
    try:
        with UnitOfWork() as uow:
            repo = SessionRepository(uow.session)
            session_entity = SessionModel(title="Failing Session", description="Will rollback", state="INIT")
            saved = repo.save(session_entity)
            failed_id = saved.id
            raise RuntimeError("Forced error to test rollback")
    except RuntimeError:
        pass

    # Verify that the session was rolled back and does not exist in DB
    with UnitOfWork() as uow:
        repo = SessionRepository(uow.session)
        fetched = repo.get(failed_id)
        assert fetched is None


def test_soft_delete_and_pagination():
    with UnitOfWork() as uow:
        repo = MemoryRepository(uow.session)
        # Create 5 memories
        mem_ids = []
        for i in range(5):
            m = MemoryModel(content=f"Memory content {i}", category="test", importance=i)
            saved = repo.save(m)
            mem_ids.append(saved.id)

        # Soft delete the first memory
        repo.delete(mem_ids[0])

    with UnitOfWork() as uow:
        repo = MemoryRepository(uow.session)
        # Verify first memory is soft deleted (not returned by default get/list)
        assert repo.get(mem_ids[0]) is None
        assert repo.get(mem_ids[0], include_deleted=True) is not None

        # Verify pagination
        paginated = repo.paginate(page=1, page_size=2)
        assert len(paginated["items"]) == 2


def test_long_term_memory_db_integration():
    lt_memory = LongTermMemory(path="test_memory.json")
    memories = [Memory(content="Persistent architectural pattern", category="design", importance=5)]
    lt_memory.save(memories, session_id="sess_stage6")

    loaded = lt_memory.load(session_id="sess_stage6")
    assert len(loaded) > 0
    assert any("Persistent architectural pattern" in m.content for m in loaded)


def test_journal_db_event_persistence():
    journal = Journal()
    event = JournalEvent(
        session_id="sess_journal_test",
        sequence_number=1,
        event_type=EventType.SESSION_CREATED,
        actor=ActorType.SYSTEM,
        payload={"title": "DB Journal Test Session"}
    )
    journal.add_event(event)

    # Query directly from database via JournalRepository
    with UnitOfWork() as uow:
        repo = JournalRepository(uow.session)
        db_events = repo.get_events_by_session("sess_journal_test")
        assert len(db_events) > 0
        assert db_events[0].event_type == "SESSION_CREATED"

from abc import ABC, abstractmethod
import json
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from sqlalchemy.orm import Session as SQLAlchemySession

from backend.app.database.connection import DatabaseConnection
from backend.app.database.models import (
    AtherOSBaseModel,
    GraphEdgeModel,
    GraphNodeModel,
    JournalEventModel,
    MemoryModel,
    PlanModel,
    SessionModel,
)

T = TypeVar("T", bound=AtherOSBaseModel)


class UnitOfWork:
    """
    Unit of Work Pattern.
    Executes atomic business operations inside a database transaction.
    Commits on success, automatically rolls back on error.
    """

    def __init__(self, db_connection: Optional[DatabaseConnection] = None):
        self.db = db_connection or DatabaseConnection()
        self.session: Optional[SQLAlchemySession] = None

    def __enter__(self) -> "UnitOfWork":
        self.session = self.db.get_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.session:
            return
        if exc_type is not None:
            self.session.rollback()
            self.session.close()
            return False
        else:
            try:
                self.session.commit()
            except Exception:
                self.session.rollback()
                raise
            finally:
                self.session.close()


class BaseRepository(ABC, Generic[T]):
    """
    Abstract Generic Repository Interface.
    Decouples core business logic from SQLAlchemy implementation details.
    """

    def __init__(self, session: SQLAlchemySession, model_cls: Type[T]):
        self.session = session
        self.model_cls = model_cls

    def save(self, entity: T) -> T:
        self.session.add(entity)
        self.session.flush()
        return entity

    def get(self, entity_id: str, include_deleted: bool = False) -> Optional[T]:
        query = self.session.query(self.model_cls).filter(self.model_cls.id == str(entity_id))
        if not include_deleted:
            query = query.filter(self.model_cls.is_deleted == False)
        return query.first()

    def list(self, limit: int = 100, offset: int = 0, include_deleted: bool = False) -> List[T]:
        query = self.session.query(self.model_cls)
        if not include_deleted:
            query = query.filter(self.model_cls.is_deleted == False)
        return query.offset(offset).limit(limit).all()

    def update(self, entity: T) -> T:
        entity.version += 1
        self.session.merge(entity)
        self.session.flush()
        return entity

    def delete(self, entity_id: str) -> bool:
        """Soft Delete entity by ID."""
        entity = self.get(entity_id)
        if entity:
            entity.is_deleted = True
            entity.version += 1
            self.session.flush()
            return True
        return False

    def count(self, include_deleted: bool = False) -> int:
        query = self.session.query(self.model_cls)
        if not include_deleted:
            query = query.filter(self.model_cls.is_deleted == False)
        return query.count()

    def exists(self, entity_id: str) -> bool:
        return self.get(entity_id) is not None

    def paginate(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        items = self.list(limit=page_size, offset=offset)
        total = self.count()
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": (total + page_size - 1) // page_size if page_size > 0 else 1
        }


class SessionRepository(BaseRepository[SessionModel]):
    def __init__(self, session: SQLAlchemySession):
        super().__init__(session, SessionModel)

    def get_active_sessions(self) -> List[SessionModel]:
        return self.session.query(SessionModel).filter(
            SessionModel.is_deleted == False,
            SessionModel.state.in_(["INIT", "PLANNING", "EXECUTING", "WAITING_FOR_INPUT"])
        ).all()


class JournalRepository(BaseRepository[JournalEventModel]):
    def __init__(self, session: SQLAlchemySession):
        super().__init__(session, JournalEventModel)

    def get_events_by_session(self, session_id: str) -> List[JournalEventModel]:
        return self.session.query(JournalEventModel).filter(
            JournalEventModel.session_id == str(session_id),
            JournalEventModel.is_deleted == False
        ).order_by(JournalEventModel.sequence_number.asc()).all()


class MemoryRepository(BaseRepository[MemoryModel]):
    def __init__(self, session: SQLAlchemySession):
        super().__init__(session, MemoryModel)

    def search_memories(self, query_text: str, category: Optional[str] = None, limit: int = 50) -> List[MemoryModel]:
        q = self.session.query(MemoryModel).filter(MemoryModel.is_deleted == False)
        if category:
            q = q.filter(MemoryModel.category == category)
        if query_text:
            q = q.filter(MemoryModel.content.ilike(f"%{query_text}%"))
        return q.order_by(MemoryModel.importance.desc()).limit(limit).all()


class PlanRepository(BaseRepository[PlanModel]):
    def __init__(self, session: SQLAlchemySession):
        super().__init__(session, PlanModel)

    def get_by_session(self, session_id: str) -> Optional[PlanModel]:
        return self.session.query(PlanModel).filter(
            PlanModel.session_id == str(session_id),
            PlanModel.is_deleted == False
        ).order_by(PlanModel.created_at.desc()).first()


class GraphNodeRepository(BaseRepository[GraphNodeModel]):
    def __init__(self, session: SQLAlchemySession):
        super().__init__(session, GraphNodeModel)

    def get_by_type(self, node_type: str, limit: int = 100) -> List[GraphNodeModel]:
        return self.session.query(GraphNodeModel).filter(
            GraphNodeModel.node_type == str(node_type),
            GraphNodeModel.is_deleted == False
        ).limit(limit).all()


class GraphEdgeRepository(BaseRepository[GraphEdgeModel]):
    def __init__(self, session: SQLAlchemySession):
        super().__init__(session, GraphEdgeModel)

    def get_outgoing(self, source_id: str) -> List[GraphEdgeModel]:
        return self.session.query(GraphEdgeModel).filter(
            GraphEdgeModel.source_id == str(source_id),
            GraphEdgeModel.is_deleted == False
        ).all()

    def get_incoming(self, target_id: str) -> List[GraphEdgeModel]:
        return self.session.query(GraphEdgeModel).filter(
            GraphEdgeModel.target_id == str(target_id),
            GraphEdgeModel.is_deleted == False
        ).all()

    def find_edge(self, source_id: str, target_id: str, relation_type: str) -> Optional[GraphEdgeModel]:
        return self.session.query(GraphEdgeModel).filter(
            GraphEdgeModel.source_id == str(source_id),
            GraphEdgeModel.target_id == str(target_id),
            GraphEdgeModel.relation_type == str(relation_type),
            GraphEdgeModel.is_deleted == False
        ).first()

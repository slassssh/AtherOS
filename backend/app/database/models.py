from datetime import datetime, UTC
import json
from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, Index, Integer, String, Text
from backend.app.database.connection import Base


class AtherOSBaseModel(Base):
    """
    Base ORM class providing enterprise fields for all entities:
    UUID primary key, timestamps, version counter, metadata JSON, and soft delete flag.
    """
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False)
    version = Column(Integer, default=1, nullable=False)
    metadata_json = Column(Text, default="{}", nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)

    def get_metadata(self) -> dict:
        try:
            return json.loads(self.metadata_json or "{}")
        except Exception:
            return {}

    def set_metadata(self, data: dict) -> None:
        self.metadata_json = json.dumps(data or {})


class SessionModel(AtherOSBaseModel):
    __tablename__ = "sessions"

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    state = Column(String(50), nullable=False, index=True)

    __table_args__ = (
        Index("idx_sessions_created_at", "created_at"),
        Index("idx_sessions_state", "state"),
    )


class JournalEventModel(AtherOSBaseModel):
    __tablename__ = "journal_events"

    session_id = Column(String(36), nullable=True, index=True)
    sequence_number = Column(Integer, nullable=False)
    event_type = Column(String(100), nullable=False, index=True)
    actor = Column(String(50), nullable=False)
    priority = Column(String(20), default="NORMAL", nullable=False)
    payload_json = Column(Text, default="{}", nullable=False)

    __table_args__ = (
        Index("idx_events_session_seq", "session_id", "sequence_number"),
        Index("idx_events_type_created", "event_type", "created_at"),
    )


class MemoryModel(AtherOSBaseModel):
    __tablename__ = "memories"

    session_id = Column(String(36), nullable=True, index=True)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    importance = Column(Integer, default=1, nullable=False)
    memory_type = Column(String(50), default="long_term", nullable=False, index=True)

    __table_args__ = (
        Index("idx_memories_cat_type", "category", "memory_type"),
        Index("idx_memories_session", "session_id"),
    )


class PlanModel(AtherOSBaseModel):
    __tablename__ = "plans"

    session_id = Column(String(36), nullable=True, index=True)
    goal = Column(Text, nullable=False)
    status = Column(String(50), default="PENDING", nullable=False, index=True)
    tasks_json = Column(Text, default="[]", nullable=False)

    __table_args__ = (
        Index("idx_plans_status_created", "status", "created_at"),
    )


class GraphNodeModel(AtherOSBaseModel):
    __tablename__ = "graph_nodes"

    node_type = Column(String(50), nullable=False, index=True)
    label = Column(String(255), nullable=False)
    properties_json = Column(Text, default="{}", nullable=False)

    __table_args__ = (
        Index("idx_nodes_type_label", "node_type", "label"),
    )


class GraphEdgeModel(AtherOSBaseModel):
    __tablename__ = "graph_edges"

    source_id = Column(String(36), nullable=False, index=True)
    target_id = Column(String(36), nullable=False, index=True)
    relation_type = Column(String(50), nullable=False, index=True)
    weight = Column(Integer, default=1, nullable=False)
    properties_json = Column(Text, default="{}", nullable=False)

    __table_args__ = (
        Index("idx_edges_src_tgt", "source_id", "target_id"),
        Index("idx_edges_rel_src", "relation_type", "source_id"),
    )

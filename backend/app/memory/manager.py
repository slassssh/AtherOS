import json
from typing import Any, Dict, List, Optional
from uuid import uuid4

from backend.app.database.models import MemoryModel
from backend.app.database.repository import MemoryRepository, UnitOfWork
from backend.app.memory.memory_item import MemoryItem
from backend.app.memory.ranker import MemoryRanker
from backend.app.utils.logger import logger


class MemoryManager:
    """
    Enterprise Central Memory Manager for AtherOS.
    The Engine communicates ONLY with MemoryManager for storing, retrieving, ranking,
    merging, summarizing, and archiving memory across all 7 memory layers:
    1. Session Memory
    2. Working Memory
    3. Project Memory
    4. Long-Term Memory
    5. Episodic Memory
    6. Semantic Memory
    7. Tool Memory
    """

    def __init__(self):
        # In-Memory stores for high-speed layers (session, working, tool)
        self._in_memory_store: Dict[str, MemoryItem] = {}

    def store(self, item: MemoryItem) -> str:
        """Stores a MemoryItem in appropriate layer and persists to database if long-term/episodic/semantic."""
        self._in_memory_store[item.memory_id] = item

        # Persist to relational database for durable layers
        if item.layer in ("long_term", "episodic", "semantic", "project"):
            try:
                with UnitOfWork() as uow:
                    repo = MemoryRepository(uow.session)
                    model = MemoryModel(
                        id=item.memory_id,
                        session_id=item.session_id,
                        content=item.content,
                        category=item.layer,
                        importance=item.importance,
                        memory_type=item.layer,
                        metadata_json=json.dumps({
                            "source": item.source,
                            "project_id": item.project_id,
                            "tags": item.tags,
                            "embedding_ready": item.embedding_ready,
                            "metadata": item.metadata,
                        })
                    )
                    repo.save(model)
            except Exception as err:
                logger.warning(f"Memory persistence warning: {err}")

        return item.memory_id

    def retrieve(self, memory_id: str) -> Optional[MemoryItem]:
        """Retrieves a MemoryItem by ID from in-memory cache or database."""
        if memory_id in self._in_memory_store:
            return self._in_memory_store[memory_id]

        try:
            with UnitOfWork() as uow:
                repo = MemoryRepository(uow.session)
                model = repo.get(memory_id)
                if model:
                    meta = model.get_metadata()
                    item = MemoryItem(
                        memory_id=model.id,
                        content=model.content,
                        layer=model.memory_type,
                        session_id=model.session_id,
                        project_id=meta.get("project_id"),
                        importance=model.importance,
                        tags=meta.get("tags", []),
                        source=meta.get("source", "SYSTEM"),
                        embedding_ready=meta.get("embedding_ready", True),
                        metadata=meta.get("metadata", {}),
                        timestamp=model.created_at
                    )
                    self._in_memory_store[item.memory_id] = item
                    return item
        except Exception as err:
            logger.warning(f"Memory retrieval error: {err}")

        return None

    def search(
        self,
        query: str = "",
        layer: Optional[str] = None,
        session_id: Optional[str] = None,
        project_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        importance: Optional[int] = None,
        limit: int = 50
    ) -> List[MemoryItem]:
        """
        Multi-criteria search across in-memory and persistent database layers.
        Applies MemoryRanker composite scoring.
        """
        candidates: List[MemoryItem] = list(self._in_memory_store.values())

        # Load additional persistent memories from database
        try:
            with UnitOfWork() as uow:
                repo = MemoryRepository(uow.session)
                models = repo.search_memories(query_text=query, category=layer, limit=limit * 2)
                for m in models:
                    if m.id not in self._in_memory_store:
                        meta = m.get_metadata()
                        item = MemoryItem(
                            memory_id=m.id,
                            content=m.content,
                            layer=m.memory_type,
                            session_id=m.session_id,
                            project_id=meta.get("project_id"),
                            importance=m.importance,
                            tags=meta.get("tags", []),
                            source=meta.get("source", "SYSTEM"),
                            metadata=meta.get("metadata", {}),
                            timestamp=m.created_at
                        )
                        candidates.append(item)
        except Exception as err:
            logger.warning(f"Database search fallback: {err}")

        # Filter candidates
        filtered: List[MemoryItem] = []
        for item in candidates:
            if layer and item.layer != layer:
                continue
            if session_id and item.session_id and item.session_id != session_id:
                continue
            if project_id and item.project_id and item.project_id != project_id:
                continue
            if importance and item.importance < importance:
                continue
            if tags:
                if not any(t in item.tags for t in tags):
                    continue
            filtered.append(item)

        # Rank using MemoryRanker composite score
        return MemoryRanker.rank(filtered, query=query, limit=limit)

    def summarize(self, session_id: str) -> str:
        """Generates a concise summary of memories associated with a session."""
        memories = self.search(session_id=session_id, limit=20)
        if not memories:
            return "No memory records found for session."

        contents = [f"- [{m.layer.upper()}] ({m.source}): {m.content}" for m in memories]
        return f"Session Summary ({len(memories)} items):\n" + "\n".join(contents)

    def archive(self, memory_id: str) -> bool:
        """Archives a memory by moving it to long_term layer."""
        item = self.retrieve(memory_id)
        if not item:
            return False
        item.layer = "long_term"
        self.store(item)
        return True

    def forget(self, memory_id: str) -> bool:
        """Soft deletes a memory item from memory cache and database."""
        if memory_id in self._in_memory_store:
            del self._in_memory_store[memory_id]

        try:
            with UnitOfWork() as uow:
                repo = MemoryRepository(uow.session)
                return repo.delete(memory_id)
        except Exception as err:
            logger.warning(f"Memory forget error: {err}")
            return False

    def merge(self, memory_ids: List[str]) -> Optional[MemoryItem]:
        """Merges multiple memory items into a single consolidated MemoryItem."""
        items = [self.retrieve(mid) for mid in memory_ids if self.retrieve(mid)]
        if not items:
            return None

        combined_content = "\n---\n".join([item.content for item in items])
        max_importance = max([item.importance for item in items])
        combined_tags = list(set([t for item in items for t in item.tags]))

        merged_item = MemoryItem(
            content=combined_content,
            layer=items[0].layer,
            source="ENGINE_MERGE",
            session_id=items[0].session_id,
            project_id=items[0].project_id,
            importance=max_importance,
            tags=combined_tags,
            metadata={"merged_from": memory_ids}
        )

        self.store(merged_item)

        # Soft delete merged sources
        for mid in memory_ids:
            self.forget(mid)

        return merged_item

    def prioritize(self, memory_id: str, new_importance: int) -> bool:
        """Updates the importance score of a memory item."""
        item = self.retrieve(memory_id)
        if not item:
            return False
        item.importance = min(max(new_importance, 1), 10)
        self.store(item)
        return True

    def stats(self) -> dict:
        """Return layer-by-layer memory statistics for health reporting."""
        layers = ["session", "working", "project", "long_term", "episodic", "semantic", "tool"]
        layer_counts = {layer: 0 for layer in layers}
        for item in self._in_memory_store.values():
            if item.layer in layer_counts:
                layer_counts[item.layer] += 1
        return {
            "total_items": len(self._in_memory_store),
            "layer_counts": layer_counts,
        }

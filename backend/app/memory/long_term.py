import json
from pathlib import Path
from typing import List, Optional

from backend.app.database.models import MemoryModel
from backend.app.database.repository import MemoryRepository, UnitOfWork
from backend.app.memory.model import Memory


class LongTermMemory:
    """
    Persistent Long-Term Memory Storage.
    Uses UnitOfWork and MemoryRepository to store memories in SQLite/Relational DB.
    """

    def __init__(self, path: str = "memory.json"):
        self.path = Path(path)

    def save(self, memories: List[Memory], session_id: Optional[str] = None) -> None:
        with UnitOfWork() as uow:
            repo = MemoryRepository(uow.session)
            for mem in memories:
                model = MemoryModel(
                    session_id=session_id,
                    content=mem.content,
                    category=mem.category,
                    importance=mem.importance,
                    memory_type="long_term"
                )
                repo.save(model)

        # File backup for backward compatibility
        try:
            data = [{"content": m.content, "category": m.category, "importance": m.importance} for m in memories]
            self.path.write_text(json.dumps(data, indent=4))
        except Exception:
            pass

    def load(self, session_id: Optional[str] = None) -> List[Memory]:
        try:
            with UnitOfWork() as uow:
                repo = MemoryRepository(uow.session)
                models = repo.search_memories(query_text="", limit=1000)
                if models:
                    return [
                        Memory(content=m.content, category=m.category, importance=m.importance)
                        for m in models
                    ]
        except Exception:
            pass

        if not self.path.exists():
            return []

        try:
            data = json.loads(self.path.read_text())
            return [Memory(content=item["content"], category=item["category"], importance=item["importance"]) for item in data]
        except Exception:
            return []
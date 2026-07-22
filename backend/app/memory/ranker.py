from datetime import datetime, UTC
import math
from typing import List, Tuple
from backend.app.memory.memory_item import MemoryItem


class MemoryRanker:
    """
    Retrieval Ranking Engine for Hierarchical Memory.
    Ranks memories by composite score: Importance + Recency Decay + Keyword Relevance.
    """

    @staticmethod
    def calculate_score(item: MemoryItem, query: str = "") -> float:
        # 1. Importance score (normalized 0 to 1)
        importance_norm = min(max(item.importance, 1), 10) / 10.0

        # 2. Recency score (decay over hours)
        now = datetime.now(UTC)
        item_time = item.timestamp if item.timestamp.tzinfo else item.timestamp.replace(tzinfo=UTC)
        age_hours = max((now - item_time).total_seconds() / 3600.0, 0.0)
        recency_score = math.exp(-age_hours / 168.0)  # half-life ~1 week

        # 3. Keyword Relevance Score
        relevance_score = 0.0
        if query:
            query_words = set(query.lower().split())
            content_words = set(item.content.lower().split())
            tag_words = set(" ".join(item.tags).lower().split())
            all_words = content_words.union(tag_words)

            if query_words and all_words:
                overlap = len(query_words.intersection(all_words))
                relevance_score = overlap / len(query_words)

        # Composite Weighted Score
        return (0.4 * importance_norm) + (0.3 * recency_score) + (0.3 * relevance_score)

    @classmethod
    def rank(cls, items: List[MemoryItem], query: str = "", limit: int = 50) -> List[MemoryItem]:
        scored: List[Tuple[MemoryItem, float]] = []
        for item in items:
            score = cls.calculate_score(item, query)
            scored.append((item, score))

        # Sort descending by composite score
        scored.sort(key=lambda x: x[1], reverse=True)
        return [item for item, _ in scored[:limit]]
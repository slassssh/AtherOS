"""
AtherOS Memory Ranker

Ranks memories by importance.
"""


class MemoryRanker:


    def rank(
        self,
        memories
    ):


        return sorted(
            memories,
            key=lambda memory:
                memory.importance,
            reverse=True
        )
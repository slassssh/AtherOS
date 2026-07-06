"""
AtherOS Memory Retriever

Retrieves memories by filters.
"""


class MemoryRetriever:


    def __init__(
        self,
        memories
    ):

        self.memories = memories


    def by_category(
        self,
        category: str
    ):


        return [
            memory
            for memory in self.memories

            if memory.category
            ==
            category
        ]


    def important(
        self,
        minimum: int
    ):


        return [
            memory
            for memory in self.memories

            if memory.importance
            >=
            minimum
        ]
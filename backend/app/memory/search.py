"""
AtherOS Memory Search

Searches memory contents.
"""


class MemorySearch:


    def __init__(
        self,
        memories
    ):

        self.memories = memories


    def search(
        self,
        query: str
    ):


        query = query.lower()


        return [
            memory

            for memory in self.memories

            if query
            in
            memory.content.lower()
        ]
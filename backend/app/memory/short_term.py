"""
AtherOS Short Term Memory

Temporary active memory storage.
"""


from backend.app.memory.model import Memory


class ShortTermMemory:


    def __init__(
        self
    ):

        self.memories = []


    def add(
        self,
        memory: Memory
    ):

        self.memories.append(
            memory
        )


    def get_all(
        self
    ):

        return self.memories.copy()


    def clear(
        self
    ):

        self.memories.clear()
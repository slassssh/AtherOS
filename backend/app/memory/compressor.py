"""
AtherOS Memory Compressor

Reduces memory size.
"""


class MemoryCompressor:


    def compress(
        self,
        memories,
        limit: int = 5
    ):


        sorted_memories = sorted(
            memories,
            key=lambda memory:
                memory.importance,
            reverse=True
        )


        return sorted_memories[
            :limit
        ]
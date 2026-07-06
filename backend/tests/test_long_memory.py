import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.memory.model import Memory
from backend.app.memory.long_term import LongTermMemory


store = LongTermMemory()


store.save(
    [
        Memory(
            content="Phase 5 memory saved",
            category="system",
            importance=5
        )
    ]
)


loaded = store.load()


for memory in loaded:

    print(memory.content)
    print(memory.category)
    print(memory.importance)
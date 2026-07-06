import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.memory.model import Memory
from backend.app.memory.ranker import MemoryRanker


memories = [

    Memory(
        content="Low priority",
        category="note",
        importance=1
    ),

    Memory(
        content="Critical project info",
        category="project",
        importance=10
    )

]


ranker = MemoryRanker()


ranked = ranker.rank(
    memories
)


for memory in ranked:

    print(
        memory.content
    )
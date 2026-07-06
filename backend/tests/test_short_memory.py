import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.memory.model import Memory
from backend.app.memory.short_term import ShortTermMemory


memory = ShortTermMemory()


memory.add(
    Memory(
        content="AtherOS reached Phase 5",
        category="project",
        importance=5
    )
)


for item in memory.get_all():

    print(
        item.content
    )

    print(
        item.category
    )

    print(
        item.importance
    )
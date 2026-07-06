import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.memory.model import Memory
from backend.app.memory.context import MemoryContext


memories = [

    Memory(
        content="AtherOS completed Phase 4",
        category="project",
        importance=10
    ),

    Memory(
        content="Continue Phase 5",
        category="task",
        importance=8
    )

]


context = MemoryContext()


print(
    context.build(
        memories
    )
)
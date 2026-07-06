import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.memory.model import Memory
from backend.app.memory.search import MemorySearch


memories = [

    Memory(
        content="AtherOS has a tool system",
        category="project",
        importance=5
    ),

    Memory(
        content="Python note",
        category="note",
        importance=1
    )

]


search = MemorySearch(
    memories
)


results = search.search(
    "tool"
)


for memory in results:

    print(
        memory.content
    )
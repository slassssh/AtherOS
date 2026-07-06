import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.memory.model import Memory
from backend.app.memory.compressor import MemoryCompressor


memories = [

    Memory(
        content="Small note",
        category="note",
        importance=1
    ),

    Memory(
        content="Important AtherOS milestone",
        category="project",
        importance=10
    )

]


compressor = MemoryCompressor()


compressed = compressor.compress(
    memories,
    limit=1
)


for memory in compressed:

    print(
        memory.content
    )
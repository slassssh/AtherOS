import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.memory.model import Memory
from backend.app.memory.retriever import MemoryRetriever


memories = [

    Memory(
        content="AtherOS Phase 5",
        category="project",
        importance=5
    ),


    Memory(
        content="Random note",
        category="note",
        importance=1
    )

]


retriever = MemoryRetriever(
    memories
)


print(
    retriever.by_category(
        "project"
    )[0].content
)


print(
    retriever.important(
        3
    )[0].importance
)
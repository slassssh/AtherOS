import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.memory.model import Memory
from backend.app.memory.summarizer import MemorySummarizer


memories = [

    Memory(
        content="Phase 4 completed",
        category="project",
        importance=10
    ),

    Memory(
        content="Started Memory Fabric",
        category="project",
        importance=9
    )

]


summarizer = MemorySummarizer()


print(
    summarizer.summarize(
        memories
    )
)
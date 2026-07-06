import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.memory.model import Memory
from backend.app.memory.short_term import ShortTermMemory
from backend.app.memory.search import MemorySearch
from backend.app.memory.ranker import MemoryRanker
from backend.app.memory.context import MemoryContext
from backend.app.memory.sync import MemorySync
from backend.app.memory.backup import MemoryBackup
from backend.app.memory.security import MemorySecurity


short = ShortTermMemory()


short.add(
    Memory(
        content="AtherOS Memory Fabric Complete",
        category="system",
        importance=10
    )
)


memories = short.get_all()


search = MemorySearch(
    memories
)


results = search.search(
    "Fabric"
)


ranker = MemoryRanker()


ranked = ranker.rank(
    results
)


context = MemoryContext()


memory_context = context.build(
    ranked
)


sync = MemorySync()


synced = sync.sync(
    ranked,
    []
)


backup = MemoryBackup()


backup.backup(
    [
        memory_context
    ],
    "memory_backup.json"
)


security = MemorySecurity()


print(memory_context)

print(
    len(synced)
)

print(
    backup.restore(
        "memory_backup.json"
    )
)

print(
    security.allowed()
)
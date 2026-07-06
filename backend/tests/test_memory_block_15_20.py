import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.memory.error_memory import ErrorMemory
from backend.app.memory.timeline import MemoryTimeline
from backend.app.memory.relationships import MemoryRelationships
from backend.app.memory.knowledge_graph import KnowledgeGraph
from backend.app.memory.importance import ImportanceScorer
from backend.app.memory.expiry import MemoryExpiry
from backend.app.memory.model import Memory


error = ErrorMemory()

error.remember(
    "Crash",
    "Restart"
)


timeline = MemoryTimeline()

timeline.add_event(
    "Phase 5 Started"
)


relation = MemoryRelationships()

relation.connect(
    "Phase4",
    "Phase5"
)


graph = KnowledgeGraph()

graph.add(
    "AtherOS",
    {
        "type": "AI OS"
    }
)


memory = Memory(
    content="Important",
    category="test",
    importance=10
)


scorer = ImportanceScorer()

expiry = MemoryExpiry()


print(error.all()[0]["solution"])

print(timeline.history()[0])

print(relation.get("Phase4"))

print(graph.find("AtherOS"))

print(scorer.score(memory))

print(expiry.expired(memory))
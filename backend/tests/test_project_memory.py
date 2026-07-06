import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.memory.project_memory import ProjectMemory


memory = ProjectMemory()


memory.save_project(
    "AtherOS",
    {
        "phase": 5,
        "status": "building"
    }
)


project = memory.get_project(
    "AtherOS"
)


print(
    project["phase"]
)


print(
    project["status"]
)
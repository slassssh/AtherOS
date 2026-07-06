import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.memory.task_memory import TaskMemory


memory = TaskMemory()


memory.save_task(
    "task_1",
    {
        "name": "Build Memory Fabric",
        "status": "running"
    }
)


task = memory.get_task(
    "task_1"
)


print(
    task["name"]
)


print(
    task["status"]
)
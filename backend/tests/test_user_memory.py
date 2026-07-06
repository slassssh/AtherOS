import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from backend.app.memory.user_memory import UserMemory


memory = UserMemory()


memory.remember(
    "project",
    "AtherOS"
)


memory.remember(
    "style",
    "build fast"
)


print(
    memory.recall(
        "project"
    )
)


print(
    memory.recall(
        "style"
    )
)
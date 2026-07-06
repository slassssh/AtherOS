"""
AtherOS Memory Backup

Backup and restore memories.
"""


import json
from pathlib import Path


class MemoryBackup:


    def backup(
        self,
        memories,
        path
    ):


        Path(path).write_text(
            json.dumps(
                memories
            )
        )


        return True


    def restore(
        self,
        path
    ):


        return json.loads(
            Path(path).read_text()
        )
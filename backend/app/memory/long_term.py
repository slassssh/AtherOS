"""
AtherOS Long Term Memory

Persistent memory storage.
"""


import json

from pathlib import Path


from backend.app.memory.model import Memory


class LongTermMemory:


    def __init__(
        self,
        path="memory.json"
    ):

        self.path = Path(
            path
        )


    def save(
        self,
        memories: list[Memory]
    ):


        data = []


        for memory in memories:


            data.append(
                {
                    "content": memory.content,
                    "category": memory.category,
                    "importance": memory.importance
                }
            )


        self.path.write_text(
            json.dumps(
                data,
                indent=4
            )
        )


    def load(
        self
    ):


        if not self.path.exists():

            return []


        data = json.loads(
            self.path.read_text()
        )


        return [
            Memory(
                content=item["content"],
                category=item["category"],
                importance=item["importance"]
            )

            for item in data
        ]
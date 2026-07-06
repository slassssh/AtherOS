"""
AtherOS Memory Relationships

Links memories together.
"""


class MemoryRelationships:


    def __init__(self):

        self.links = {}


    def connect(
        self,
        source,
        target
    ):

        self.links[
            source
        ] = target


    def get(
        self,
        source
    ):

        return self.links.get(
            source
        )
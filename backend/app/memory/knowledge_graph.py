"""
AtherOS Knowledge Graph

Stores connected knowledge nodes.
"""


class KnowledgeGraph:


    def __init__(self):

        self.nodes = {}


    def add(
        self,
        name,
        data
    ):

        self.nodes[
            name
        ] = data


    def find(
        self,
        name
    ):

        return self.nodes.get(
            name
        )
"""
AtherOS Project Memory

Stores project states.
"""


class ProjectMemory:


    def __init__(
        self
    ):

        self.projects = {}


    def save_project(
        self,
        name: str,
        data: dict
    ):


        self.projects[
            name
        ] = data


    def get_project(
        self,
        name: str
    ):


        return self.projects.get(
            name
        )
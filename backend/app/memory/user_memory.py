"""
AtherOS User Memory

Stores user related information.
"""


class UserMemory:


    def __init__(
        self
    ):

        self.profile = {}


    def remember(
        self,
        key: str,
        value
    ):


        self.profile[
            key
        ] = value


    def recall(
        self,
        key: str
    ):


        return self.profile.get(
            key
        )
"""
AtherOS Memory Security

Controls memory access.
"""


class MemorySecurity:


    def __init__(
        self
    ):

        self.locked = False


    def lock(
        self
    ):

        self.locked = True


    def allowed(
        self
    ):

        return not self.locked
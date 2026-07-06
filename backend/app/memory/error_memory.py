"""
AtherOS Error Memory

Stores errors and solutions.
"""


class ErrorMemory:


    def __init__(self):

        self.errors = []


    def remember(
        self,
        error: str,
        solution: str
    ):

        self.errors.append(
            {
                "error": error,
                "solution": solution
            }
        )


    def all(self):

        return self.errors.copy()
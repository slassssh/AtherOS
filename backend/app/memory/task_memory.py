"""
AtherOS Task Memory

Tracks remembered tasks.
"""


class TaskMemory:


    def __init__(
        self
    ):

        self.tasks = {}


    def save_task(
        self,
        task_id: str,
        data: dict
    ):


        self.tasks[
            task_id
        ] = data


    def get_task(
        self,
        task_id: str
    ):


        return self.tasks.get(
            task_id
        )
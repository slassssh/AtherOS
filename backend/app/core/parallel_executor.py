"""
AtherOS Parallel Executor

Runs multiple tools concurrently.
"""


import asyncio

from backend.app.core.async_executor import AsyncToolExecutor


class ParallelExecutor:


    def __init__(
        self,
        executor: AsyncToolExecutor
    ):

        self.executor = executor


    async def execute_many(
        self,
        tasks: list[dict]
    ):

        jobs = []


        for task in tasks:

            jobs.append(
                self.executor.execute_async(
                    task["tool"],
                    **task["args"]
                )
            )


        results = await asyncio.gather(
            *jobs
        )


        return results
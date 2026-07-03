"""
AtherOS Async Executor

Runs tools asynchronously.
"""


import asyncio

from backend.app.core.tool_executor import ToolExecutor


class AsyncToolExecutor:


    def __init__(
        self,
        executor: ToolExecutor
    ):

        self.executor = executor


    async def execute_async(
        self,
        tool_name: str,
        **kwargs
    ):

        result = await asyncio.to_thread(
            self.executor.execute,
            tool_name,
            **kwargs
        )


        return result
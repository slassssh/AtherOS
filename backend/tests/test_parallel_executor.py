import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


from backend.app.tools.registry import ToolRegistry
from backend.app.tools.python_tool import PythonTool

from backend.app.core.tool_executor import ToolExecutor
from backend.app.core.async_executor import AsyncToolExecutor
from backend.app.core.parallel_executor import ParallelExecutor


async def main():

    registry = ToolRegistry()

    registry.register(
        PythonTool()
    )


    executor = ToolExecutor(
        registry
    )


    async_executor = AsyncToolExecutor(
        executor
    )


    parallel = ParallelExecutor(
        async_executor
    )


    results = await parallel.execute_many(
        [
            {
                "tool": "python",
                "args": {
                    "code": "print('Task 1')"
                }
            },
            {
                "tool": "python",
                "args": {
                    "code": "print('Task 2')"
                }
            }
        ]
    )


    for result in results:
        print(result)


asyncio.run(main())
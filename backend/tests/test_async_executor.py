import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


from backend.app.core.tool_executor import ToolExecutor
from backend.app.core.async_executor import AsyncToolExecutor

from backend.app.tools.registry import ToolRegistry
from backend.app.tools.python_tool import PythonTool


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


    result = await async_executor.execute_async(
        "python",
        code="print('Async AtherOS')"
    )


    print(result)


asyncio.run(main())
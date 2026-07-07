import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


from app.core.production import ProductionCore
from app.core.event_bus import AsyncEventBus
from app.core.auth import Authentication
from app.core.agent_loop import AgentRuntimeLoop
from app.core.observability import Observability

import asyncio



def test_phase11_complete():


    # production launch

    production = ProductionCore()

    result = production.launch()

    assert result["production"]
    assert result["secure"]



    # async event system

    async def event_test():

        bus = AsyncEventBus()


        async def handler(data):

            return data


        bus.subscribe(
            "boot",
            handler
        )


        result = await bus.publish(
            "boot",
            "online"
        )


        assert result[0] == "online"



    asyncio.run(
        event_test()
    )



    # security

    auth = Authentication()

    auth.register(
        "admin",
        "pass"
    )


    assert auth.login(
        "admin",
        "pass"
    )



    # runtime loop

    loop = AgentRuntimeLoop()

    loop.start()

    assert loop.tick()["executed"]



    # observability

    observer = Observability()

    observer.emit(
        "healthy"
    )


    assert "healthy" in observer.metrics()



if __name__ == "__main__":

    test_phase11_complete()


    print(
        "🎉 AtherOS v1.1 Production Core Complete"
    )
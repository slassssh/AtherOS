import sys
import os
import asyncio


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


from app.core.event_bus import AsyncEventBus
from app.core.storage import PersistentStorage
from app.core.container import Container
from app.core.plugins import PluginManager
from app.core.api_layer import APILayer



def test_phase11_core():


    async def event_test():

        bus = AsyncEventBus()


        async def handler(data):

            return data


        bus.subscribe(
            "start",
            handler
        )


        result = await bus.publish(
            "start",
            "hello"
        )


        assert result[0] == "hello"



    asyncio.run(
        event_test()
    )



    storage = PersistentStorage(
        "test_store.json"
    )


    storage.save(
        "mode",
        "auto"
    )


    assert storage.load(
        "mode"
    ) == "auto"



    container = Container()

    container.register(
        "db",
        object()
    )


    assert container.resolve(
        "db"
    )



    plugins = PluginManager()

    plugins.load(
        "security",
        object()
    )


    assert "security" in plugins.all()



    api = APILayer()

    api.route(
        "/health",
        lambda: "ok"
    )


    assert api.execute(
        "/health"
    ) == "ok"



if __name__ == "__main__":

    test_phase11_core()

    print(
        "✅ Phase 11 Block 1 (Features 1-5) Production Core Tests Passed"
    )
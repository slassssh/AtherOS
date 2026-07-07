import asyncio


class AsyncEventBus:


    def __init__(self):

        self.listeners = {}


    def subscribe(self, event, handler):

        if event not in self.listeners:
            self.listeners[event] = []

        self.listeners[event].append(
            handler
        )

        return True



    async def publish(self, event, data):

        results = []

        for handler in self.listeners.get(
            event,
            []
        ):

            result = await handler(
                data
            )

            results.append(
                result
            )


        return results
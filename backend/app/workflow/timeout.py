import time


class TimeoutPolicy:


    def execute(self, function, limit):

        start = time.time()

        result = function()

        elapsed = (
            time.time() - start
        )


        return {
            "result": result,
            "timeout": elapsed > limit
        }
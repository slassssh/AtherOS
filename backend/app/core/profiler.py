import time


class PerformanceProfiler:


    def measure(self, function):

        start = time.time()

        result = function()

        end = time.time()


        return {
            "result": result,
            "duration": end - start
        }
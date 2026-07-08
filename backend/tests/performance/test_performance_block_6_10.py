import os
import sys


sys.path.append(
    os.path.abspath(".")
)


from backend.app.performance.scheduler import SchedulerOptimizer
from backend.app.performance.async_engine import AsyncEngine
from backend.app.performance.load_balancer import LoadBalancer
from backend.app.performance.monitor import ResourceMonitor
from backend.app.performance.profiler import PerformanceProfiler



def test_execution_performance():


    assert SchedulerOptimizer().optimize()["scheduler_optimized"]


    assert AsyncEngine().enable()["async_enabled"]


    assert LoadBalancer().balance()["balanced"]


    assert ResourceMonitor().status()["monitoring"]


    assert PerformanceProfiler().profile()["profile_created"]




if __name__ == "__main__":

    test_execution_performance()


    print(
        "✅ Phase 23 Block 2 (Features 6-10) Performance Tests Passed"
    )
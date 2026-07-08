import os
import sys


sys.path.append(
    os.path.abspath(".")
)


from backend.app.performance.core import PerformanceCore
from backend.app.performance.cpu import CPUOptimizer
from backend.app.performance.memory import MemoryOptimizer
from backend.app.performance.cache import CacheOptimizer
from backend.app.performance.startup import StartupOptimizer



def test_performance_foundation():


    assert PerformanceCore().status()["performance_enabled"]


    assert CPUOptimizer().optimize()["cpu_optimized"]


    assert MemoryOptimizer().optimize()["memory_optimized"]


    assert CacheOptimizer().optimize()["cache_optimized"]


    assert StartupOptimizer().optimize()["startup_optimized"]




if __name__ == "__main__":

    test_performance_foundation()


    print(
        "✅ Phase 23 Block 1 (Features 1-5) Performance Tests Passed"
    )
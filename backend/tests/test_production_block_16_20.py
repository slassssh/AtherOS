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


from app.core.profiler import PerformanceProfiler
from app.core.cache import Cache
from app.core.resource_limits import ResourceLimiter
from app.core.tracing import ErrorTracer
from app.core.observability import Observability



def test_phase11_observability_layer():


    profiler = PerformanceProfiler()

    result = profiler.measure(
        lambda: "done"
    )

    assert result["result"] == "done"



    cache = Cache()

    cache.set(
        "mode",
        "auto"
    )

    assert cache.get(
        "mode"
    ) == "auto"



    limiter = ResourceLimiter(
        100
    )

    assert limiter.allow(
        50
    )



    tracer = ErrorTracer()

    tracer.capture(
        Exception("fail")
    )

    assert len(
        tracer.all()
    ) == 1



    observer = Observability()

    observer.emit(
        "healthy"
    )

    assert "healthy" in observer.metrics()



if __name__ == "__main__":

    test_phase11_observability_layer()

    print(
        "✅ Phase 11 Block 4 (Features 16-20) Observability Tests Passed"
    )
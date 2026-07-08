import os
import sys


sys.path.append(
    os.path.abspath(".")
)


from backend.app.performance.bottleneck import BottleneckDetector
from backend.app.performance.auto_tuner import AutoTuner
from backend.app.performance.analytics import PerformanceAnalytics
from backend.app.performance.integration import PerformanceIntegration



def test_performance_final_layer():


    assert BottleneckDetector().detect()["bottleneck_scan"]


    assert AutoTuner().tune()["auto_tuned"]


    assert PerformanceAnalytics().analyze()["analytics"]


    result = PerformanceIntegration().launch()


    assert result["running"]

    assert result["analytics"]

    assert result["optimized"]




if __name__ == "__main__":

    test_performance_final_layer()


    print(
        "✅ Phase 23 Block 3 (Features 11-15) Performance Tests Passed"
    )
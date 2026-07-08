import os
import sys


sys.path.append(
    os.path.abspath(".")
)


from backend.app.beta.feedback import FeedbackCollector
from backend.app.beta.crash import CrashReporter
from backend.app.beta.analytics import BetaAnalytics
from backend.app.beta.integration import BetaIntegration



def test_beta_final_layer():


    assert FeedbackCollector().collect()["feedback_collected"]


    assert CrashReporter().report()["crash_reporting"]


    assert BetaAnalytics().analyze()["analytics_enabled"]


    result = BetaIntegration().launch()


    assert result["running"]

    assert result["analytics"]

    assert result["feedback"]




if __name__ == "__main__":

    test_beta_final_layer()


    print(
        "✅ Phase 26 Block 2 (Features 6-10) Beta Tests Passed"
    )
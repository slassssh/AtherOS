import os
import sys


sys.path.append(
    os.path.abspath(".")
)


from backend.app.testing.core import TestingCore
from backend.app.testing.unit import UnitTestEngine
from backend.app.testing.integration import IntegrationTestEngine
from backend.app.testing.regression import RegressionTesting
from backend.app.testing.runner import TestRunner



def test_testing_foundation():


    assert TestingCore().status()["testing_enabled"]


    assert UnitTestEngine().run()["unit_tests"]


    assert IntegrationTestEngine().run()["integration_tests"]


    assert RegressionTesting().run()["regression_passed"]


    assert TestRunner().execute()["executed"]




if __name__ == "__main__":

    test_testing_foundation()


    print(
        "✅ Phase 24 Block 1 (Features 1-5) Testing Infrastructure Tests Passed"
    )
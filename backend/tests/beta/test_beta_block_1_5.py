import os
import sys


sys.path.append(
    os.path.abspath(".")
)


from backend.app.beta.core import BetaCore
from backend.app.beta.release import ReleaseManager
from backend.app.beta.build import BuildSystem
from backend.app.beta.environment import EnvironmentChecker
from backend.app.beta.compatibility import CompatibilityValidator



def test_beta_foundation():


    assert BetaCore().status()["beta_enabled"]


    assert ReleaseManager().prepare()["release_ready"]


    assert BuildSystem().build()["build_success"]


    assert EnvironmentChecker().check()["environment_valid"]


    assert CompatibilityValidator().validate()["compatible"]




if __name__ == "__main__":

    test_beta_foundation()


    print(
        "✅ Phase 26 Block 1 (Features 1-5) Beta Tests Passed"
    )
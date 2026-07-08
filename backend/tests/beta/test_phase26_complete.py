import os
import sys


sys.path.append(
    os.path.abspath(".")
)


from backend.app.beta.core import BetaCore
from backend.app.beta.release import ReleaseManager
from backend.app.beta.build import BuildSystem
from backend.app.beta.integration import BetaIntegration



def test_phase26_complete():


    assert BetaCore().status()["beta_enabled"]


    assert ReleaseManager().prepare()["release_ready"]


    assert BuildSystem().build()["build_success"]


    result = BetaIntegration().launch()


    assert result["running"]

    assert result["analytics"]

    assert result["feedback"]




if __name__ == "__main__":

    test_phase26_complete()


    print(
        "🎉 Phase 26 Beta Release Complete"
    )
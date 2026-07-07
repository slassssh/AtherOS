import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.developer.core import CodeWorkspaceCore
from backend.app.developer.repo_analyzer import RepositoryAnalyzer
from backend.app.developer.code_generator import CodeGenerator
from backend.app.developer.integration import DeveloperIntegration



def test_phase16_complete():


    core = CodeWorkspaceCore()

    assert core.start()["active"]



    repo = RepositoryAnalyzer()

    assert repo.analyze(
        "AtherOS"
    )["analyzed"]



    generator = CodeGenerator()

    assert generator.generate(
        "build feature"
    )["generated"]



    final = DeveloperIntegration()

    result = final.launch()


    assert result["running"]

    assert result["secure"]




if __name__ == "__main__":

    test_phase16_complete()


    print(
        "🎉 Phase 16 Developer Workspace Complete"
    )
import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.developer.core import CodeWorkspaceCore
from backend.app.developer.repo_analyzer import RepositoryAnalyzer
from backend.app.developer.code_parser import CodeParser
from backend.app.developer.symbol_extractor import SymbolExtractor
from backend.app.developer.dependency_analyzer import DependencyAnalyzer



def test_developer_foundation():


    core = CodeWorkspaceCore()

    assert core.start()["active"]



    repo = RepositoryAnalyzer()

    assert repo.analyze(
        "AtherOS"
    )["analyzed"]



    parser = CodeParser()

    assert parser.parse(
        "print()"
    )["parsed"]



    symbols = SymbolExtractor()

    assert "class" in symbols.extract(
        "class Agent"
    )["symbols"]



    deps = DependencyAnalyzer()

    assert deps.analyze(
        ["fastapi"]
    )["checked"]




if __name__ == "__main__":

    test_developer_foundation()


    print(
        "✅ Phase 16 Block 1 (Features 1-5) Developer Tests Passed"
    )
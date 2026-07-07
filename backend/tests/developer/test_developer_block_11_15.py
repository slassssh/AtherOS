import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.developer.debug_assistant import DebugAssistant
from backend.app.developer.error_analyzer import ErrorAnalyzer
from backend.app.developer.fix_suggestions import FixSuggestions
from backend.app.developer.refactor_engine import RefactorEngine
from backend.app.developer.code_generator import CodeGenerator



def test_developer_intelligence():


    debugger = DebugAssistant()

    assert debugger.debug(
        "crash"
    )["debugged"]



    error = ErrorAnalyzer()

    assert error.analyze(
        "ImportError"
    )["cause_found"]



    fix = FixSuggestions()

    assert fix.suggest(
        "bug"
    )["fix"] == "suggested"



    refactor = RefactorEngine()

    assert refactor.refactor(
        "code"
    )["optimized"]



    generator = CodeGenerator()

    assert generator.generate(
        "create API"
    )["generated"]




if __name__ == "__main__":

    test_developer_intelligence()


    print(
        "✅ Phase 16 Block 3 (Features 11-15) Developer Tests Passed"
    )
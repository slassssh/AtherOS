import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.developer.ai_context import AICodeContext
from backend.app.developer.code_search import CodeSearch
from backend.app.developer.code_memory import CodeMemory
from backend.app.developer.terminal import TerminalIntegration
from backend.app.developer.command_assistant import CommandAssistant



def test_developer_ai_layer():


    context = AICodeContext()

    context.add(
        "project",
        "AtherOS"
    )

    assert context.get(
        "project"
    ) == "AtherOS"



    search = CodeSearch()

    search.index(
        "agent.py"
    )

    assert "agent.py" in search.search(
        "agent"
    )



    memory = CodeMemory()

    memory.remember(
        "bug fix"
    )

    assert "bug fix" in memory.recall()



    terminal = TerminalIntegration()

    assert terminal.execute(
        "python app.py"
    )["executed"]



    assistant = CommandAssistant()

    assert assistant.suggest(
        "run server"
    )["suggestion"] == "command generated"




if __name__ == "__main__":

    test_developer_ai_layer()


    print(
        "✅ Phase 16 Block 2 (Features 6-10) Developer Tests Passed"
    )
import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from desktop.app.ui.chat_interface import ChatInterface
from desktop.app.ui.ai_console import AIConsole
from desktop.app.ui.streaming_ui import StreamingUI
from desktop.app.ui.context_viewer import ContextViewer
from desktop.app.ui.session_viewer import SessionViewer



def test_ai_ui_layer():


    chat = ChatInterface()

    assert chat.send(
        "hello"
    )["sent"]

    assert "hello" in chat.history()



    console = AIConsole()

    assert console.run_prompt(
        "think"
    ) == "Processed: think"



    stream = StreamingUI()

    stream.push(
        "Ath"
    )

    stream.push(
        "erOS"
    )

    assert stream.output() == "AtherOS"



    context = ContextViewer()

    context.update(
        "goal",
        "build"
    )


    assert context.view()["goal"] == "build"



    sessions = SessionViewer()

    sessions.add(
        "session-1"
    )


    assert "session-1" in sessions.all()



if __name__ == "__main__":

    test_ai_ui_layer()


    print(
        "✅ v1.3 Desktop UI Block 3 (Features 11-15) Tests Passed"
    )
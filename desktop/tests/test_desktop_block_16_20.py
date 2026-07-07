import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from desktop.app.ui.file_explorer import FileExplorer
from desktop.app.ui.code_workspace import CodeWorkspace
from desktop.app.ui.terminal_panel import TerminalPanel
from desktop.app.ui.task_board import TaskBoard
from desktop.app.ui.notification_center import NotificationCenter



def test_workspace_ui():


    files = FileExplorer()

    files.add_file(
        "main.py"
    )

    assert "main.py" in files.list_files()



    code = CodeWorkspace()

    code.open_project(
        "AtherOS"
    )

    assert "AtherOS" in code.active_projects()



    terminal = TerminalPanel()

    result = terminal.execute(
        "run"
    )

    assert result["status"] == "completed"



    board = TaskBoard()

    board.add_task(
        "build-ui"
    )

    assert "build-ui" in board.show()



    notify = NotificationCenter()

    notify.notify(
        "done"
    )

    assert "done" in notify.all()



if __name__ == "__main__":

    test_workspace_ui()


    print(
        "✅ v1.3 Desktop UI Block 4 (Features 16-20) Tests Passed"
    )
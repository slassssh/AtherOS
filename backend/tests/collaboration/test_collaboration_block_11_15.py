import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.collaboration.chat import TeamChat
from backend.app.collaboration.notifications import TeamNotifications
from backend.app.collaboration.tasks import TaskAssignment
from backend.app.collaboration.approval import ApprovalSystem
from backend.app.collaboration.version import VersionCollaboration



def test_team_communication():


    chat = TeamChat()

    chat.send(
        "hello team"
    )


    assert "hello team" in chat.history()



    assert TeamNotifications().notify(
        "update"
    )["sent"]



    assert TaskAssignment().assign(
        "build",
        "agent"
    )["assigned"]



    assert ApprovalSystem().approve(
        "merge"
    )["approved"]



    assert VersionCollaboration().sync(
        "v1"
    )["synced"]




if __name__ == "__main__":

    test_team_communication()


    print(
        "✅ Phase 21 Block 3 (Features 11-15) Collaboration Tests Passed"
    )
import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.collaboration.core import TeamCore
from backend.app.collaboration.users import UserManagement
from backend.app.collaboration.roles import MemberRoles
from backend.app.collaboration.permissions import TeamPermissions
from backend.app.collaboration.workspace import TeamWorkspace



def test_team_foundation():


    assert TeamCore().status()["team_enabled"]


    assert UserManagement().add(
        "user"
    )["added"]


    assert MemberRoles().assign(
        "user",
        "admin"
    )["assigned"]


    assert TeamPermissions().allow(
        "write"
    )["allowed"]


    assert TeamWorkspace().create(
        "AtherOS-Team"
    )["created"]




if __name__ == "__main__":

    test_team_foundation()


    print(
        "✅ Phase 21 Block 1 (Features 1-5) Collaboration Tests Passed"
    )
import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.collaboration.projects import SharedProjects
from backend.app.collaboration.realtime import RealTimeCollaboration
from backend.app.collaboration.presence import PresenceSystem
from backend.app.collaboration.comments import CommentsSystem
from backend.app.collaboration.activity import ActivityFeed



def test_team_collaboration():


    assert SharedProjects().share(
        "AtherOS"
    )["shared"]



    assert RealTimeCollaboration().connect()["realtime"]



    assert PresenceSystem().status(
        "user"
    )["online"]



    comments = CommentsSystem()

    comments.add(
        "hello"
    )


    assert "hello" in comments.all()



    activity = ActivityFeed()

    activity.add(
        "commit"
    )


    assert "commit" in activity.all()




if __name__ == "__main__":

    test_team_collaboration()


    print(
        "✅ Phase 21 Block 2 (Features 6-10) Collaboration Tests Passed"
    )
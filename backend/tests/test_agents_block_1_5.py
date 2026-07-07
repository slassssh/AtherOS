import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.agents.registry import AgentRegistry
from app.agents.identity import AgentIdentity
from app.agents.profile import AgentProfile
from app.agents.roles import AgentRoles
from app.agents.permissions import AgentPermissions



def test_phase8_agents_core():


    identity = AgentIdentity(
        "security-agent"
    )


    info = identity.info()

    assert info["name"] == "security-agent"



    registry = AgentRegistry()

    registry.register(
        info["id"],
        identity
    )

    assert registry.get(
        info["id"]
    )


    profile = AgentProfile(
        info["id"]
    )

    profile.update(
        "level",
        "advanced"
    )

    assert profile.get(
        "level"
    ) == "advanced"



    roles = AgentRoles()

    roles.assign(
        info["id"],
        "defender"
    )

    assert roles.get_role(
        info["id"]
    ) == "defender"



    permissions = AgentPermissions()

    permissions.allow(
        info["id"],
        "scan"
    )


    assert permissions.can_execute(
        info["id"],
        "scan"
    )



if __name__ == "__main__":

    test_phase8_agents_core()

    print(
        "✅ Phase 8 Block 1 (Features 1-5) Agent Core Tests Passed"
    )
import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.security_suite.agent_binding import AgentSecurityBinding
from backend.app.security_suite.workflow_binding import WorkflowSecurityBinding
from backend.app.security_suite.plugin_binding import PluginSecurityBinding
from backend.app.security_suite.intelligence import SecurityIntelligence
from backend.app.security_suite.controller import SecurityController



def test_security_orchestration():


    assert AgentSecurityBinding().bind(
        "agent"
    )["secured"]


    assert WorkflowSecurityBinding().bind(
        "workflow"
    )["secured"]


    assert PluginSecurityBinding().bind(
        "plugin"
    )["secured"]


    assert SecurityIntelligence().analyze()["ai_security"]


    assert SecurityController().start()["running"]




if __name__ == "__main__":

    test_security_orchestration()


    print(
        "✅ Phase 19 Block 4 (Features 16-20) Security Tests Passed"
    )
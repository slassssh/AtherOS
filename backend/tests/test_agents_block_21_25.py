import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.agents.metrics import MultiAgentMetrics
from app.agents.logs import MultiAgentLogs
from app.agents.security import MultiAgentSecurity
from app.agents.controller import MultiAgentController
from app.agents.integration import MultiAgentIntegration



def test_phase8_final_layer():


    metrics = MultiAgentMetrics()

    metrics.record(
        "count",
        5
    )

    assert metrics.get(
        "count"
    ) == 5



    logs = MultiAgentLogs()

    logs.add(
        "started"
    )

    assert len(
        logs.history()
    ) == 1



    security = MultiAgentSecurity()

    security.block_agent(
        "bad-agent"
    )

    assert security.trusted(
        "bad-agent"
    ) == False



    controller = MultiAgentController()

    assert controller.start()

    assert controller.status()



    system = MultiAgentIntegration()

    result = system.launch()

    assert result["running"]

    assert result["secure"]



if __name__ == "__main__":

    test_phase8_final_layer()

    print(
        "✅ Phase 8 Block 5 (Features 21-25) Final Tests Passed"
    )
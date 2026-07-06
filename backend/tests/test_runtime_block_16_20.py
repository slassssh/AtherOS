import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.runtime.memory_bridge import MemoryIntegration
from app.runtime.tool_bridge import ToolIntegration
from app.runtime.intelligence_bridge import IntelligenceIntegration
from app.runtime.error_recovery import RuntimeErrorRecovery
from app.runtime.event_stream import EventStream



def test_phase7_runtime_integrations():


    memory = MemoryIntegration()

    assert memory.store(
        "cycle completed"
    )

    assert len(memory.recall()) == 1



    tools = ToolIntegration()

    tools.register(
        "scanner",
        object()
    )

    assert "scanner" in tools.available()



    ai = IntelligenceIntegration()

    decision = ai.decide(
        "security event"
    )

    assert decision["decision"] == "approved"



    recovery = RuntimeErrorRecovery()

    recovery.capture(
        Exception("failure")
    )

    assert recovery.recover()["recovered"]



    stream = EventStream()

    event = stream.emit(
        "agent_started"
    )

    assert event["event"] == "agent_started"



if __name__ == "__main__":

    test_phase7_runtime_integrations()

    print(
        "✅ Phase 7 Block 4 (Features 16-20) Integration Tests Passed"
    )
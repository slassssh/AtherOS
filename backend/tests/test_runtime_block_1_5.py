import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.runtime.agent_runtime import AgentRuntime
from app.runtime.runtime_state import RuntimeStateMachine, RuntimeState
from app.runtime.session_manager import AgentSessionManager
from app.runtime.lifecycle import AgentLifecycle
from app.runtime.runtime_context import RuntimeContext



def test_phase7_runtime_block():

    runtime = AgentRuntime()

    assert runtime.start() == "runtime_started"

    result = runtime.execute_cycle()

    assert result["executed"] == True

    assert runtime.stop() == "runtime_stopped"



    state = RuntimeStateMachine()

    state.transition(RuntimeState.RUNNING)

    assert state.current() == "running"



    manager = AgentSessionManager()

    sid = manager.create_session()

    assert manager.get_session(sid)["active"] == True

    assert manager.close_session(sid)



    life = AgentLifecycle()

    assert life.boot()

    assert life.shutdown()

    assert len(life.history()) == 2



    ctx = RuntimeContext()

    ctx.set("goal", "build")

    assert ctx.get("goal") == "build"

    assert ctx.remove("goal")



if __name__ == "__main__":

    test_phase7_runtime_block()

    print(
        "✅ Phase 7 Block 1 (Features 1-5) Runtime Tests Passed"
    )
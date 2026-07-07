import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


from app.workflow.step_executor import StepExecutor
from app.workflow.conditional import ConditionalStep
from app.workflow.parallel import ParallelSteps
from app.workflow.retry import RetryPolicy
from app.workflow.timeout import TimeoutPolicy



def test_phase9_execution_engine():


    executor = StepExecutor()

    result = executor.execute(
        "scan"
    )

    assert result["success"]



    conditional = ConditionalStep()

    result = conditional.run_if(
        True,
        "repair"
    )

    assert result["executed"]



    parallel = ParallelSteps()

    results = parallel.execute_all(
        [
            "scan",
            "monitor"
        ]
    )

    assert len(results) == 2



    retry = RetryPolicy()

    result = retry.attempt(
        lambda: "success"
    )

    assert result == "success"



    timeout = TimeoutPolicy()

    result = timeout.execute(
        lambda: "done",
        5
    )

    assert result["timeout"] == False



if __name__ == "__main__":

    test_phase9_execution_engine()

    print(
        "✅ Phase 9 Block 2 (Features 6-10) Execution Tests Passed"
    )
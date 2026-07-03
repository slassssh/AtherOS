"""
AtherOS Tool Metrics

Tracks tool usage statistics.
"""


from dataclasses import dataclass


@dataclass
class ToolMetrics:

    executions: int = 0

    successes: int = 0

    failures: int = 0


    def record_success(self):

        self.executions += 1
        self.successes += 1


    def record_failure(self):

        self.executions += 1
        self.failures += 1
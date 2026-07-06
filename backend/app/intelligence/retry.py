"""
AtherOS Retry Logic

Handles failed attempts.
"""


class RetryEngine:


    def should_retry(
        self,
        attempts: int,
        limit: int = 3
    ):


        return attempts < limit
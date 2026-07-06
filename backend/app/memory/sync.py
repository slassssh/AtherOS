"""
AtherOS Memory Sync

Synchronizes memory states.
"""


class MemorySync:


    def sync(
        self,
        source,
        target
    ):

        target.extend(
            source
        )


        return target
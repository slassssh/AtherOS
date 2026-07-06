"""
AtherOS Memory Context

Injects memories into runtime context.
"""


class MemoryContext:


    def build(
        self,
        memories
    ):


        context = ""


        for memory in memories:


            context += (
                memory.content
                +
                "\n"
            )


        return context
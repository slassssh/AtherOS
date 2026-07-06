"""
AtherOS Memory Summarizer

Creates summaries from memories.
"""


class MemorySummarizer:


    def summarize(
        self,
        memories
    ):


        contents = [
            memory.content

            for memory in memories
        ]


        return " | ".join(
            contents
        )
class DocumentChunker:


    def chunk(self, text, size=5):

        return [
            text[i:i+size]
            for i in range(
                0,
                len(text),
                size
            )
        ]
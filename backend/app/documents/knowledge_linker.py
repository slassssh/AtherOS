class KnowledgeLinker:


    def __init__(self):

        self.links = []



    def link(self, source, target):

        self.links.append(
            (
                source,
                target
            )
        )


        return True



    def all(self):

        return self.links
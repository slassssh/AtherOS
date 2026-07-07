class DocumentLoader:


    def __init__(self):

        self.documents = []



    def load(self, document):

        self.documents.append(document)

        return True



    def all(self):

        return self.documents
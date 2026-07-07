class DocumentBinding:


    def __init__(self):

        self.documents = []



    def attach(self, document):

        self.documents.append(document)

        return True



    def all(self):

        return self.documents
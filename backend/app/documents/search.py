class DocumentSearch:


    def __init__(self):

        self.documents = []



    def add(self, document):

        self.documents.append(document)

        return True



    def search(self, keyword):

        return [
            doc
            for doc in self.documents
            if keyword in doc
        ]
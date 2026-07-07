class DocumentIndexer:


    def __init__(self):

        self.index = {}



    def add(self, name, content):

        self.index[name] = content

        return True



    def get(self, name):

        return self.index.get(name)
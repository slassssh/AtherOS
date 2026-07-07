class CodeSearch:


    def __init__(self):

        self.files = []



    def index(self, file):

        self.files.append(file)

        return True



    def search(self, keyword):

        return [
            file
            for file in self.files
            if keyword in file
        ]
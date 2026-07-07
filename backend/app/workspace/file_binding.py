class FileBinding:


    def __init__(self):

        self.files = []



    def bind(self, file):

        self.files.append(
            file
        )

        return True



    def all(self):

        return self.files
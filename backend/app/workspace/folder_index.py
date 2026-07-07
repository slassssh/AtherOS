class FolderIndex:


    def __init__(self):

        self.index = []



    def add_folder(self, folder):

        self.index.append(
            folder
        )

        return True



    def folders(self):

        return self.index
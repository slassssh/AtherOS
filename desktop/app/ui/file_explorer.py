class FileExplorer:


    def __init__(self):

        self.files = []



    def add_file(self, file):

        self.files.append(
            file
        )


        return True



    def list_files(self):

        return self.files
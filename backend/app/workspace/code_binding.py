class CodeBinding:


    def __init__(self):

        self.repositories = []



    def attach(self, repo):

        self.repositories.append(repo)

        return True



    def all(self):

        return self.repositories
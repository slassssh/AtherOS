class WorkspaceSearch:


    def __init__(self):

        self.items = []



    def add(self, item):

        self.items.append(
            item
        )

        return True



    def find(self, keyword):

        return [
            item
            for item in self.items
            if keyword in item
        ]
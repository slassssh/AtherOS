class SnapshotManager:


    def __init__(self):

        self.snapshots = {}



    def create(self, name, data):

        self.snapshots[name] = data


        return True



    def get(self, name):

        return self.snapshots.get(
            name
        )
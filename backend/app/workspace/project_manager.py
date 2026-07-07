class ProjectManager:


    def __init__(self):

        self.projects = []



    def create(self, name):

        self.projects.append(
            name
        )

        return True



    def list_projects(self):

        return self.projects
class CodeWorkspace:


    def __init__(self):

        self.projects = []



    def open_project(self, project):

        self.projects.append(
            project
        )


        return True



    def active_projects(self):

        return self.projects
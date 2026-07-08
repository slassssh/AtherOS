class PackageRegistry:

    def __init__(self):

        self.packages = []

    def register(self, package):

        self.packages.append(package)

        return True

    def all(self):

        return self.packages
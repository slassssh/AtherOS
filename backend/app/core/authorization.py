class Authorization:


    def __init__(self):

        self.permissions = {}


    def grant(self, user, permission):

        self.permissions.setdefault(
            user,
            []
        )

        self.permissions[user].append(
            permission
        )

        return True



    def allowed(self, user, permission):

        return permission in self.permissions.get(
            user,
            []
        )
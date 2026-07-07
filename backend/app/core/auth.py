import hashlib


class Authentication:


    def __init__(self):

        self.users = {}


    def register(self, username, password):

        hashed = hashlib.sha256(
            password.encode()
        ).hexdigest()


        self.users[username] = hashed

        return True



    def login(self, username, password):

        hashed = hashlib.sha256(
            password.encode()
        ).hexdigest()


        return self.users.get(
            username
        ) == hashed
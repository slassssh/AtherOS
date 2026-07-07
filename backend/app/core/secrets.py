class SecretsManager:


    def __init__(self):

        self.secrets = {}


    def store(self, key, value):

        self.secrets[key] = value

        return True



    def get(self, key):

        return self.secrets.get(
            key
        )
import base64


class Encryption:


    def encrypt(self, data):

        return base64.b64encode(
            data.encode()
        ).decode()



    def decrypt(self, token):

        return base64.b64decode(
            token.encode()
        ).decode()
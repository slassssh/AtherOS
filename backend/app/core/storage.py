import json
import os


class PersistentStorage:


    def __init__(self, file="storage.json"):

        self.file = file


    def save(self, key, value):

        data = {}

        if os.path.exists(self.file):

            with open(
                self.file,
                "r"
            ) as f:

                data = json.load(f)


        data[key] = value


        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                data,
                f
            )


        return True



    def load(self, key):

        if not os.path.exists(
            self.file
        ):

            return None


        with open(
            self.file,
            "r"
        ) as f:

            data = json.load(f)


        return data.get(
            key
        )
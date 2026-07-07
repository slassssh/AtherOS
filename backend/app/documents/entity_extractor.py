class EntityExtractor:


    def extract(self, text):

        words = text.split()


        return {
            "entities": words
        }
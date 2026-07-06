class ThinkModule:

    def __init__(self):
        self.thoughts = []


    def think(self, observation):

        result = {
            "input": observation,
            "analysis": "processed"
        }

        self.thoughts.append(result)

        return result


    def history(self):

        return self.thoughts
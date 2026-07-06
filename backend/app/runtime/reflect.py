class ReflectModule:

    def __init__(self):
        self.reflections = []


    def reflect(self, action_result):

        reflection = {
            "result": action_result,
            "learning": "stored"
        }

        self.reflections.append(reflection)

        return reflection


    def history(self):

        return self.reflections
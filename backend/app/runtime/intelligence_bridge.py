class IntelligenceIntegration:

    def __init__(self):

        self.decisions = []


    def decide(self, context):

        decision = {
            "context": context,
            "decision": "approved"
        }

        self.decisions.append(decision)

        return decision


    def history(self):

        return self.decisions
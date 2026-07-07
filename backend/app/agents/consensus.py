class ConsensusSystem:

    def __init__(self):

        self.votes = []


    def vote(self, decision):

        self.votes.append(decision)

        return True


    def consensus(self):

        approvals = self.votes.count(
            True
        )

        return approvals > len(self.votes) / 2
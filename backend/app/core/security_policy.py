class SecurityPolicy:


    def __init__(self):

        self.rules = []


    def add_rule(self, rule):

        self.rules.append(
            rule
        )

        return True



    def validate(self, rule):

        return rule in self.rules
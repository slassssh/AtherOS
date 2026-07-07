class IdentityGuard:


    def verify(self, identity):

        return {
            "identity": identity,
            "verified": True
        }
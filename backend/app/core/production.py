from app.core.cli import AtherCLI
from app.core.sdk import AtherSDK
from app.core.observability import Observability
from app.core.security_policy import SecurityPolicy


class ProductionCore:


    def __init__(self):

        self.cli = AtherCLI()
        self.sdk = AtherSDK()
        self.observer = Observability()
        self.security = SecurityPolicy()



    def launch(self):

        self.observer.emit(
            "production-online"
        )


        self.security.add_rule(
            "secure"
        )


        return {
            "production": True,
            "secure": True
        }
import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


from app.core.auth import Authentication
from app.core.authorization import Authorization
from app.core.secrets import SecretsManager
from app.core.encryption import Encryption
from app.core.security_policy import SecurityPolicy



def test_phase11_security_layer():


    auth = Authentication()

    auth.register(
        "admin",
        "123"
    )

    assert auth.login(
        "admin",
        "123"
    )



    access = Authorization()

    access.grant(
        "admin",
        "execute"
    )

    assert access.allowed(
        "admin",
        "execute"
    )



    secrets = SecretsManager()

    secrets.store(
        "api",
        "key"
    )

    assert secrets.get(
        "api"
    ) == "key"



    crypto = Encryption()

    encrypted = crypto.encrypt(
        "data"
    )

    assert crypto.decrypt(
        encrypted
    ) == "data"



    policy = SecurityPolicy()

    policy.add_rule(
        "safe-mode"
    )

    assert policy.validate(
        "safe-mode"
    )



if __name__ == "__main__":

    test_phase11_security_layer()

    print(
        "✅ Phase 11 Block 2 (Features 6-10) Security Tests Passed"
    )
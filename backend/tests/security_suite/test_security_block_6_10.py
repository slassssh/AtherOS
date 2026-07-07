import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.security_suite.encryption import EncryptionManager
from backend.app.security_suite.secrets import SecretsVault
from backend.app.security_suite.policy import PolicyEngine
from backend.app.security_suite.permission_analyzer import PermissionAnalyzer
from backend.app.security_suite.audit import AuditLogger



def test_security_governance():


    encryption = EncryptionManager()

    assert encryption.encrypt(
        "data"
    )["encrypted"]



    vault = SecretsVault()

    vault.store(
        "token",
        "123"
    )


    assert vault.get(
        "token"
    ) == "123"



    policy = PolicyEngine()

    assert policy.enforce(
        "zero-trust"
    )["enforced"]



    permissions = PermissionAnalyzer()

    assert permissions.analyze(
        "admin"
    )["safe"]



    audit = AuditLogger()

    audit.log(
        "login"
    )


    assert "login" in audit.all()




if __name__ == "__main__":

    test_security_governance()


    print(
        "✅ Phase 19 Block 2 (Features 6-10) Security Tests Passed"
    )
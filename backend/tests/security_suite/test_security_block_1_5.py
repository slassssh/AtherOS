import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.security_suite.core import SecurityCore
from backend.app.security_suite.threat_scanner import ThreatScanner
from backend.app.security_suite.vulnerability import VulnerabilityScanner
from backend.app.security_suite.access_monitor import AccessMonitor
from backend.app.security_suite.identity_guard import IdentityGuard



def test_security_core():


    assert SecurityCore().status()["security_active"]


    assert ThreatScanner().scan()["safe"]


    assert VulnerabilityScanner().check()["secure"]


    assert AccessMonitor().monitor(
        "admin"
    )["allowed"]


    assert IdentityGuard().verify(
        "agent"
    )["verified"]




if __name__ == "__main__":

    test_security_core()


    print(
        "✅ Phase 19 Block 1 (Features 1-5) Security Tests Passed"
    )
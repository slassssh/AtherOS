import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from backend.app.security_suite.intrusion import IntrusionDetection
from backend.app.security_suite.risk import RiskEngine
from backend.app.security_suite.compliance import ComplianceChecker
from backend.app.security_suite.reports import SecurityReports
from backend.app.security_suite.incident_response import IncidentResponse



def test_security_response():


    intrusion = IntrusionDetection()

    assert intrusion.detect(
        "network"
    )["protected"]



    risk = RiskEngine()

    assert risk.calculate(
        "server"
    )["risk_score"] == 0



    compliance = ComplianceChecker()

    assert compliance.verify()["compliant"]



    reports = SecurityReports()

    assert reports.generate()["report_created"]



    incident = IncidentResponse()

    assert incident.respond(
        "attack"
    )["resolved"]




if __name__ == "__main__":

    test_security_response()


    print(
        "✅ Phase 19 Block 3 (Features 11-15) Security Tests Passed"
    )
from backend.app.documents.security import DocumentSecurity
from backend.app.documents.metrics import DocumentMetrics



class DocumentIntegration:


    def __init__(self):

        self.security = DocumentSecurity()
        self.metrics = DocumentMetrics()



    def start(self):

        self.metrics.record(
            "documents",
            "active"
        )


        return {
            "running": True,
            "secure": self.security.scan(
                "system"
            )["secure"]
        }
from backend.app.documentation.controller import DocumentationController
from backend.app.documentation.ai_assistant import DocumentationAIAssistant
from backend.app.documentation.metrics import DocumentationMetrics



class DocumentationIntegration:


    def __init__(self):

        self.controller = DocumentationController()
        self.ai = DocumentationAIAssistant()
        self.metrics = DocumentationMetrics()



    def launch(self):

        self.controller.start()


        return {
            "running": self.controller.running,
            "ai_enabled": self.ai.help()["ai_docs_enabled"],
            "metrics": self.metrics.analyze()["metrics_enabled"]
        }
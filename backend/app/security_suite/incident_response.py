class IncidentResponse:


    def respond(self, incident):

        return {
            "incident": incident,
            "resolved": True
        }
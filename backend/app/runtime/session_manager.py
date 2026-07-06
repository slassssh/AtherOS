from datetime import datetime
import uuid


class AgentSessionManager:

    def __init__(self):
        self.sessions = {}

    def create_session(self):

        session_id = str(uuid.uuid4())

        self.sessions[session_id] = {
            "created": datetime.utcnow(),
            "active": True
        }

        return session_id


    def close_session(self, session_id):

        if session_id in self.sessions:
            self.sessions[session_id]["active"] = False
            return True

        return False


    def get_session(self, session_id):
        return self.sessions.get(session_id)
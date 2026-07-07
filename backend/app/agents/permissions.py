class AgentPermissions:


    def __init__(self):

        self.permissions = {}


    def allow(self, agent_id, action):

        self.permissions.setdefault(
            agent_id,
            []
        )

        self.permissions[agent_id].append(
            action
        )

        return True


    def can_execute(self, agent_id, action):

        return action in self.permissions.get(
            agent_id,
            []
        )